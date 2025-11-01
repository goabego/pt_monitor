import datetime
import logging
import google.auth
from google.api_core import exceptions
from google.cloud import monitoring_v3
from google.protobuf import duration_pb2
import pandas as pd

from .config.models import MetricConfig

def log_authentication_method():
    """
    Determines and logs the authentication method being used by the Google Cloud client library.
    """
    try:
        credentials, project_id = google.auth.default()
        auth_type = "Unknown"
        
        if hasattr(credentials, 'service_account_email'):
            auth_type = f"Service Account: {credentials.service_account_email}"
        elif hasattr(credentials, 'id_token'):
             auth_type = f"User Credentials" # User credentials don't expose the email directly
        
        logging.info(f"Authentication successful. Using credentials of type: {auth_type}")

    except exceptions.DefaultCredentialsError:
        logging.error("Authentication failed. Could not find default credentials.")
        logging.error("Please run 'gcloud auth application-default login' or set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during authentication: {e}")

def query_metric(
    project_id: str,
    metric_config: MetricConfig,
    days_ago_start: int = 90,
    days_ago_end: int = 0,
) -> pd.DataFrame:
    """
    Retrieves and processes a specified metric from Google Cloud Monitoring.
    """
    try:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{project_id}"

        # 1. Define Time Interval
        now = datetime.datetime.now(datetime.timezone.utc)
        end_time = now - datetime.timedelta(days=days_ago_end)
        start_time = now - datetime.timedelta(days=days_ago_start)
        interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)

        # 2. Define Metric Filter
        metric_filter = f'metric.type = "{metric_config.metric_type}"'

        # 3. Define Aggregation
        ONE_DAY_S = 86400
        
        resource_labels = [
            'resource.label.project_id', 'resource.label.location',
            'resource.label.publisher', 'resource.label.model_version_id',
            'resource.label.model_user_id',
        ]
        metric_labels = [f'metric.label.{label}' for label in metric_config.metric_labels]
        
        aligner = getattr(monitoring_v3.Aggregation.Aligner, metric_config.aligner)
        reducer = getattr(monitoring_v3.Aggregation.Reducer, metric_config.reducer)

        aggregation = monitoring_v3.Aggregation(
            alignment_period=duration_pb2.Duration(seconds=ONE_DAY_S),
            per_series_aligner=aligner,
            cross_series_reducer=reducer,
            group_by_fields=resource_labels + metric_labels,
        )

        # 4. Create and Send the Request
        logging.info(f"Querying metric: {metric_config.metric_type} from {start_time.date()} to {end_time.date()}...")
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=metric_filter,
            interval=interval,
            aggregation=aggregation,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )
        results = client.list_time_series(request=request)

        # 5. Process and Format Results
        data = []
        for time_series in results:
            row = {label: value for label, value in time_series.resource.labels.items()}
            row.update({label: value for label, value in time_series.metric.labels.items()})

            for point in time_series.points:
                point_row = row.copy()
                ts_seconds = point.interval.end_time.timestamp()
                point_row["date"] = datetime.datetime.fromtimestamp(ts_seconds).date()
                
                value = getattr(point.value, metric_config.value_field, None)
                if metric_config.value_field == "distribution_value" and value:
                    point_row[metric_config.value_name] = value.count
                else:
                    point_row[metric_config.value_name] = value

                data.append(point_row)

        if not data:
            logging.warning("No data found for the specified period.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        
        # Define the desired fixed order for the initial columns
        preferred_order = ['date', 'location', 'project_id', 'model_user_id', 'model_version_id']
        
        # Get all columns from the DataFrame
        all_cols = df.columns.tolist()
        
        # Start the final order with preferred columns that exist in the DataFrame
        final_ordered_cols = [col for col in preferred_order if col in all_cols]
        
        # Get the remaining label columns (not preferred, not the value column)
        value_col = metric_config.value_name
        remaining_labels = [
            col for col in all_cols 
            if col not in final_ordered_cols and col != value_col
        ]
        remaining_labels.sort() # Sort the rest alphabetically for consistency
        
        # Combine the lists to get the final column order
        final_ordered_cols.extend(remaining_labels)
        final_ordered_cols.append(value_col)
        
        # Reorder the DataFrame
        df = df[final_ordered_cols]
        
        # Define sorting order, respecting the new visual hierarchy
        sorting_cols = [col for col in preferred_order if col in df.columns]
        
        return df.sort_values(by=sorting_cols).reset_index(drop=True)

    except exceptions.PermissionDenied as e:
        logging.error(f"Permission denied for project '{project_id}'. Check your authentication and IAM roles.")
        logging.error(f"Details: {e}")
    except exceptions.GoogleAPICallError as e:
        logging.error(f"An API error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    
    return pd.DataFrame()

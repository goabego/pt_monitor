import argparse
import datetime
import logging
from google.api_core import exceptions
from google.cloud import monitoring_v3
from google.protobuf import duration_pb2
import pandas as pd

from metric_configs import METRIC_CONFIGS, MetricConfig

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def query_metric(
    project_id: str,
    metric_config: MetricConfig,
    days_ago_start: int = 90,
    days_ago_end: int = 0,
) -> pd.DataFrame:
    """
    Retrieves and processes a specified metric from Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud Project ID.
        metric_config: A MetricConfig object with the metric's configuration.
        days_ago_start: The start of the time window in days from now.
        days_ago_end: The end of the time window in days from now (0 is 'now').

    Returns:
        A pandas DataFrame with the queried metric data.
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
        ONE_DAY_S = 86400  # 1 day in seconds
        
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
        grouping_cols = sorted([col for col in df.columns if col != metric_config.value_name and col != 'date'])
        all_cols = ["date"] + grouping_cols + [metric_config.value_name]
        df = df[all_cols]
        return df.sort_values(by=["date"] + grouping_cols).reset_index(drop=True)

    except exceptions.PermissionDenied as e:
        logging.error(f"Permission denied for project '{project_id}'. Check your authentication and IAM roles.")
        logging.error(f"Details: {e}")
    except exceptions.GoogleAPICallError as e:
        logging.error(f"An API error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    
    return pd.DataFrame()

def main():
    parser = argparse.ArgumentParser(description="Google Cloud AI Platform Token Usage Monitor.")
    parser.add_argument(
        "--project-id", type=str, required=True, help="Your Google Cloud Project ID."
    )
    parser.add_argument(
        "--metric", type=str, choices=list(METRIC_CONFIGS.keys()),
        help="The metric to query. Required if --all-metrics is not specified."
    )
    parser.add_argument(
        "--all-metrics", action="store_true", help="Query all available metrics sequentially."
    )
    parser.add_argument(
        "--days-ago-start", type=int, default=90,
        help="The start of the time window, in days from the current time."
    )
    parser.add_argument(
        "--days-ago-end", type=int, default=0,
        help="The end of the time window, in days from the current time (0 means 'now')."
    )
    parser.add_argument(
        "--output", type=str, default="markdown", choices=["markdown", "csv", "json"],
        help="The output format for the results."
    )

    args = parser.parse_args()

    if not args.metric and not args.all_metrics:
        parser.error("Either --metric or --all-metrics must be specified.")
    
    if args.metric and args.all_metrics:
        parser.error("Specify either --metric or --all-metrics, not both.")

    def print_data(data, output_format):
        if data.empty:
            return
        if output_format == "markdown":
            print(data.to_markdown(index=False))
        elif output_format == "csv":
            print(data.to_csv(index=False))
        elif output_format == "json":
            print(data.to_json(orient="records", indent=2))

    if args.all_metrics:
        for metric_name, metric_config in METRIC_CONFIGS.items():
            logging.info(f"--- Querying Metric: {metric_name} ---")
            usage_data = query_metric(
                project_id=args.project_id,
                metric_config=metric_config,
                days_ago_start=args.days_ago_start,
                days_ago_end=args.days_ago_end,
            )
            
            # Add a header to the data output for clarity
            if not usage_data.empty:
                print(f"\n--- Metric: {metric_name} ---")
                print_data(usage_data, args.output)
            
            logging.info(f"--- End of Metric: {metric_name} ---")
    else:
        metric_config = METRIC_CONFIGS[args.metric]
        usage_data = query_metric(
            project_id=args.project_id,
            metric_config=metric_config,
            days_ago_start=args.days_ago_start,
            days_ago_end=args.days_ago_end,
        )
        print_data(usage_data, args.output)

if __name__ == "__main__":
    main()
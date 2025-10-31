import datetime
from google.cloud import monitoring_v3
from google.protobuf import duration_pb2
import pandas as pd

def get_daily_token_throughput(project_id: str, days_ago_start: int = 90, days_ago_end: int = 0) -> pd.DataFrame:
    """
    Retrieves the daily consumed token throughput for the PublisherModel resource 
    over a specified time period.

    Args:
        project_id: Your Google Cloud Project ID.
        days_ago_start: The start of the time window, in days from the current time.
        days_ago_end: The end of the time window, in days from the current time.
                      0 means 'now'.
    
    Returns:
        A pandas DataFrame with 'date' and 'consumed_tokens' columns.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    # 1. Define Time Interval
    # Use timezone-aware datetime objects as recommended
    now = datetime.datetime.now(datetime.timezone.utc)
    end_time = now - datetime.timedelta(days=days_ago_end)
    start_time = now - datetime.timedelta(days=days_ago_start)

    interval = monitoring_v3.TimeInterval(
        start_time=start_time,
        end_time=end_time,
    )

    # 2. Define Metric and Resource Filter
    # The metric type for consumed token throughput
    METRIC_TYPE = "aiplatform.googleapis.com/publisher/online_serving/consumed_token_throughput"
    # Filter for the specific metric
    metric_filter = f'metric.type = "{METRIC_TYPE}"'

    # 3. Define Aggregation for Daily Sum
    # The metric is a DELTA type (a count over a short period), so we use:
    # - ALIGN_DELTA to normalize the time series values (convert the Delta value to a Rate)
    # - REDUCE_SUM to sum all values within the alignment period
    # - ALIGNMENT_PERIOD = 86400s (1 day)
    ONE_DAY_S = 86400
    
    aggregation = monitoring_v3.Aggregation(
        alignment_period=duration_pb2.Duration(seconds=ONE_DAY_S),
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_DELTA,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
        # To prevent "N/A" values, we must group by all the labels we want to keep.
        # The API only returns labels that are part of the grouping.
        group_by_fields=[
            'resource.label.project_id',
            'resource.label.location',
            'resource.label.publisher',
            'resource.label.model_version_id',
            'resource.label.model_user_id',
            'metric.label.request_type'
        ],
    )

    # 4. Create and Send the Request
    print(f"Querying metric: {METRIC_TYPE} from {start_time.date()} to {end_time.date()}...")

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=metric_filter,
        interval=interval,
        aggregation=aggregation,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = client.list_time_series(request=request)
    
    # 5. Process and Format Results
    # resource_container: The identifier of the GCP Project owning the Endpoint.
    # location: The region in which the service is running.
    # publisher: The publisher of the model.
    # model_user_id: The resource ID of the PublisherModel.
    # model_version_id: The version ID of the PublisherModel.
    data = []
    for time_series in results:
        # Extract labels for grouping
        resource_labels = time_series.resource.labels
        resource_container = resource_labels.get("project_id", "N/A")
        location = resource_labels.get("location", "N/A")
        publisher = resource_labels.get("publisher", "N/A")
        model_user_id = resource_labels.get("model_user_id", "N/A")
        model_version_id = resource_labels.get("model_version_id", "N/A")
        request_type = time_series.metric.labels.get("request_type", "N/A")
        
        # Each point is a daily aggregate
        for point in time_series.points:
            # The end time of the interval represents the end of the day period
            ts_seconds = point.interval.end_time.timestamp()
            date = datetime.datetime.fromtimestamp(ts_seconds).date()
            # The consumed token value is INT64
            value = point.value.int64_value
            
            data.append({
                "date": date,
                "resource_container": resource_container,
                "location": location,
                "publisher": publisher,
                "model_version_id": model_version_id,
                "model_user_id": model_user_id,
                "request_type": request_type,
                "consumed_tokens": value
            })

    if not data:
        print("No data found for the specified period.")
        return pd.DataFrame(columns=["date", "resource_container", "location", "publisher", "model_version_id", "model_user_id", "request_type", "consumed_tokens"])

    df = pd.DataFrame(data)
    
    grouping_cols = [
        "date", "resource_container", "location", "publisher", "model_version_id", "model_user_id", "request_type"
    ]

    # Group by date, model, and request type to get a detailed daily breakdown.
    # This provides a more granular view than just summing by date.
    daily_breakdown = df.groupby(grouping_cols)["consumed_tokens"].sum().reset_index()
    daily_breakdown = daily_breakdown.sort_values(by=grouping_cols)

    return daily_breakdown

# --- Example Usage ---

# **IMPORTANT:** Replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID
PROJECT_ID = "agent-starter-pack-spend" 

if PROJECT_ID == "YOUR_PROJECT_ID":
    print("!!! ERROR: Please replace 'YOUR_PROJECT_ID' with your actual Project ID to run the code.")
else:
    # Default: Last 90 days to now
    usage_data = get_daily_token_throughput(PROJECT_ID)
    
    print(usage_data.to_markdown(index=False))

    # Example: Custom 7-day range (e.g., 10 days ago to 3 days ago)
    # custom_usage_data = get_daily_token_throughput(PROJECT_ID, days_ago_start=10, days_ago_end=3)
    # print("\n--- Custom 7-Day Range Usage ---")
    # print(custom_usage_data.to_markdown(index=False))

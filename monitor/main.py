import argparse
import logging
import pandas as pd

from .gcp_client import query_metric, log_authentication_method
from .charting import generate_chart
from .config.metrics import METRIC_CONFIGS

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def generate_report_charts(project_id, days_ago_start, days_ago_end, filter_model_id, metrics_with_data, metrics_without_data):
    """
    Generates a standard set of charts for key metrics.
    """
    logging.info("--- Starting Standard Chart Generation ---")
    
    report_metrics = {
        "character_count": ["type"],
        "token_count": ["type"],
        "consumed_throughput": ["model_user_id"],
        "consumed_token_throughput": ["model_user_id"],
        "model_invocation_count": ["model_user_id"],
        "model_invocation_latencies": ["latency_type"],
    }

    for metric_name, group_by_cols in report_metrics.items():
        logging.info(f"--- Processing metric: {metric_name} ---")
        metric_config = METRIC_CONFIGS.get(metric_name)
        if not metric_config:
            logging.warning(f"Metric '{metric_name}' not found in configurations. Skipping.")
            continue

        usage_data = query_metric(
            project_id=project_id,
            metric_config=metric_config,
            days_ago_start=days_ago_start,
            days_ago_end=days_ago_end,
        )

        if usage_data.empty:
            metrics_without_data.append(metric_name)
            logging.warning(f"No data returned for {metric_name}. Skipping chart generation.")
            continue

        if filter_model_id and 'model_user_id' in usage_data.columns:
            original_rows = len(usage_data)
            usage_data = usage_data[usage_data['model_user_id'] == filter_model_id]
            logging.info(f"Filtered by model_user_id '{filter_model_id}'. Kept {len(usage_data)} of {original_rows} rows.")
            if usage_data.empty:
                metrics_without_data.append(metric_name)
                logging.warning(f"No data remains for {metric_name} after filtering. Skipping chart generation.")
                continue
        
        metrics_with_data.append(metric_name)
        generate_chart(usage_data, metric_config.name, metric_config.value_name, group_by_cols)

    logging.info("--- Standard Chart Generation Complete ---")

def main():
    log_authentication_method()

    parser = argparse.ArgumentParser(description="Google Cloud AI Platform Token Usage Monitor.")
    parser.add_argument(
        "--project-id", type=str, required=True, help="Your Google Cloud Project ID."
    )
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--metric", type=str, choices=list(METRIC_CONFIGS.keys()),
        help="Query a single metric for data output."
    )
    mode_group.add_argument(
        "--all-metrics", action="store_true", 
        help="Query all available metrics sequentially for data output."
    )
    mode_group.add_argument(
        "--generate-report-charts", action="store_true",
        help="Generate a standard set of charts for key metrics."
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
        help="The output format for the results (used with --metric or --all-metrics)."
    )
    parser.add_argument(
        "--generate-graph", action="store_true",
        help="Generate a graph for a single queried metric (only used with --metric)."
    )
    parser.add_argument(
        "--graph-group-by", type=str,
        help="Comma-separated columns to group by for the graph (e.g., 'request_type,model_user_id')."
    )
    parser.add_argument(
        "--filter-model-id", type=str,
        help="Filter data by a specific model_user_id (used with --generate-report-charts)."
    )

    args = parser.parse_args()

    if args.generate_graph and not args.metric:
        parser.error("--generate-graph can only be used with the --metric flag.")
    if args.graph_group_by and not args.generate_graph:
        parser.error("--graph-group-by can only be used with --generate-graph.")
    if args.filter_model_id and not args.generate_report_charts:
        parser.error("--filter-model-id can only be used with --generate-report-charts.")

    def print_data(data, output_format):
        if data.empty:
            return
        if output_format == "markdown":
            print(data.to_markdown(index=False))
        elif output_format == "csv":
            print(data.to_csv(index=False))
        elif output_format == "json":
            print(data.to_json(orient="records", indent=2))

    metrics_with_data = []
    metrics_without_data = []

    if args.generate_report_charts:
        generate_report_charts(
            project_id=args.project_id,
            days_ago_start=args.days_ago_start,
            days_ago_end=args.days_ago_end,
            filter_model_id=args.filter_model_id,
            metrics_with_data=metrics_with_data,
            metrics_without_data=metrics_without_data
        )
    elif args.all_metrics:
        for metric_name, metric_config in METRIC_CONFIGS.items():
            logging.info(f"--- Querying Metric: {metric_name} ---")
            usage_data = query_metric(
                project_id=args.project_id,
                metric_config=metric_config,
                days_ago_start=args.days_ago_start,
                days_ago_end=args.days_ago_end,
            )
            
            if not usage_data.empty:
                metrics_with_data.append(metric_name)
                print(f"\n--- Metric: {metric_name} ---")
                print_data(usage_data, args.output)
            else:
                metrics_without_data.append(metric_name)
            
            logging.info(f"--- End of Metric: {metric_name} ---")
    elif args.metric:
        metric_config = METRIC_CONFIGS[args.metric]
        usage_data = query_metric(
            project_id=args.project_id,
            metric_config=metric_config,
            days_ago_start=args.days_ago_start,
            days_ago_end=args.days_ago_end,
        )
        
        if not usage_data.empty:
            metrics_with_data.append(args.metric)
            print_data(usage_data, args.output)
        else:
            metrics_without_data.append(args.metric)

        if args.generate_graph:
            group_by_cols = args.graph_group_by.split(',') if args.graph_group_by else []
            generate_chart(usage_data, metric_config.name, metric_config.value_name, group_by_cols)

    # --- Final Summary ---
    if len(metrics_with_data) + len(metrics_without_data) > 1:
        logging.info("\n\n--- Query Summary ---")
        if metrics_with_data:
            logging.info("Metrics with data found:")
            for metric in sorted(metrics_with_data):
                logging.info(f"  - {metric}")
        if metrics_without_data:
            logging.info("Metrics with no data:")
            for metric in sorted(metrics_without_data):
                logging.info(f"  - {metric}")
        logging.info("--- End of Summary ---")

if __name__ == "__main__":
    main()

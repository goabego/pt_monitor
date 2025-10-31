from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class MetricConfig:
    """
    A data model for defining a Google Cloud Monitoring metric configuration.
    """
    name: str
    metric_type: str
    value_field: str
    value_name: str
    metric_labels: List[str] = field(default_factory=list)
    aligner: str = "ALIGN_DELTA"
    reducer: str = "REDUCE_SUM"

# A dictionary mapping a friendly name to its MetricConfig object.
METRIC_CONFIGS = {
    # --- DELTA Metrics ---
    "character_count": MetricConfig(
        name="character_count",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/character_count",
        value_field="int64_value",
        value_name="character_count",
        metric_labels=["type", "request_type", "accounting_resource", "modality"],
    ),
    "consumed_throughput": MetricConfig(
        name="consumed_throughput",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/consumed_throughput",
        value_field="int64_value",
        value_name="consumed_throughput",
        metric_labels=["request_type", "accounting_resource", "modality"],
    ),
    "consumed_token_throughput": MetricConfig(
        name="consumed_token_throughput",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/consumed_token_throughput",
        value_field="int64_value",
        value_name="consumed_tokens",
        metric_labels=["request_type", "accounting_resource", "modality"],
    ),
    "model_invocation_count": MetricConfig(
        name="model_invocation_count",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/model_invocation_count",
        value_field="int64_value",
        value_name="invocation_count",
        metric_labels=["input_token_size", "output_token_size", "max_token_size", "response_code", "request_type", "method", "error_category", "explicit_caching", "accounting_resource"],
    ),
    "token_count": MetricConfig(
        name="token_count",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/token_count",
        value_field="int64_value",
        value_name="token_count",
        metric_labels=["max_token_size", "type", "request_type", "explicit_caching", "accounting_resource", "modality", "source"],
    ),
    # --- DISTRIBUTION Metrics (showing count) ---
    "characters": MetricConfig(
        name="characters",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/characters",
        value_field="distribution_value",
        value_name="characters_distribution_count",
        metric_labels=["type", "request_type", "accounting_resource", "modality"],
    ),
    "first_token_latencies": MetricConfig(
        name="first_token_latencies",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/first_token_latencies",
        value_field="distribution_value",
        value_name="first_token_latencies_dist_count",
        metric_labels=["input_token_size", "output_token_size", "max_token_size", "request_type", "explicit_caching"],
    ),
    "model_invocation_latencies": MetricConfig(
        name="model_invocation_latencies",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/model_invocation_latencies",
        value_field="distribution_value",
        value_name="model_invocation_latencies_dist_count",
        metric_labels=["input_token_size", "output_token_size", "max_token_size", "latency_type", "request_type", "explicit_caching"],
    ),
    "tokens": MetricConfig(
        name="tokens",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/tokens",
        value_field="distribution_value",
        value_name="tokens_distribution_count",
        metric_labels=["max_token_size", "type", "request_type", "accounting_resource", "modality"],
    ),
    # --- GAUGE Metrics ---
    "dedicated_character_limit": MetricConfig(
        name="dedicated_character_limit",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/dedicated_character_limit",
        value_field="int64_value",
        value_name="dedicated_character_limit",
        aligner="ALIGN_MEAN",
        reducer="REDUCE_MEAN",
    ),
    "dedicated_character_project_max_limit": MetricConfig(
        name="dedicated_character_project_max_limit",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/dedicated_character_project_max_limit",
        value_field="int64_value",
        value_name="dedicated_character_project_max_limit",
        metric_labels=["accounting_resource"],
        aligner="ALIGN_MEAN",
        reducer="REDUCE_MEAN",
    ),
    "dedicated_gsu_limit": MetricConfig(
        name="dedicated_gsu_limit",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/dedicated_gsu_limit",
        value_field="int64_value",
        value_name="dedicated_gsu_limit",
        aligner="ALIGN_MEAN",
        reducer="REDUCE_MEAN",
    ),
    "dedicated_gsu_project_max_limit": MetricConfig(
        name="dedicated_gsu_project_max_limit",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/dedicated_gsu_project_max_limit",
        value_field="int64_value",
        value_name="dedicated_gsu_project_max_limit",
        metric_labels=["accounting_resource"],
        aligner="ALIGN_MEAN",
        reducer="REDUCE_MEAN",
    ),
    "dedicated_token_limit": MetricConfig(
        name="dedicated_token_limit",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/dedicated_token_limit",
        value_field="int64_value",
        value_name="dedicated_token_limit",
        aligner="ALIGN_MEAN",
        reducer="REDUCE_MEAN",
    ),
    "dedicated_token_project_max_limit": MetricConfig(
        name="dedicated_token_project_max_limit",
        metric_type="aiplatform.googleapis.com/publisher/online_serving/dedicated_token_project_max_limit",
        value_field="int64_value",
        value_name="dedicated_token_project_max_limit",
        metric_labels=["accounting_resource"],
        aligner="ALIGN_MEAN",
        reducer="REDUCE_MEAN",
    ),
}

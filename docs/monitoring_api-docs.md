# Vertex AI Monitoring Specifications

This document outlines the monitored resource and available metrics for Vertex AI Model Garden Publisher Models on Google Cloud Platform.

## Monitored Resource: `aiplatform.googleapis.com/PublisherModel`

-   **Source:** [Google Cloud Monitoring API Documentation](https://cloud.google.com/monitoring/api/resources#tag_aiplatform.googleapis.com/PublisherModel)
-   **Display Name:** Vertex AI Model Garden Publisher Model
-   **Description:** A Vertex AI Model Garden Publisher Model.
-   **Resource Labels:**
    -   `resource_container`: The identifier of the GCP Project owning the Endpoint.
    -   `location`: The region in which the service is running.
    -   `publisher`: The publisher of the model.
    -   `model_user_id`: The resource ID of the PublisherModel.
    -   `model_version_id`: The version ID of the PublisherModel.

---

## Metrics for `aiplatform.googleapis.com/PublisherModel`

-   **Source:** [Google Cloud Monitoring API Metrics](https://cloud.google.com/monitoring/api/metrics_gcp_a_b#gcp-aiplatform)

### `publisher/online_serving/character_count`

-   **Status:** BETA
-   **Display Name:** Character count
-   **Description:** Accumulated input/output character count.
-   **Kind:** DELTA
-   **Value Type:** INT64
-   **Unit:** `1`
-   **Metric Labels:**
    -   `type`: Type of character (input/output).
    -   `request_type`: Type of request (dedicated/shared).
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.
    -   `modality`: Modality of the characters.

### `publisher/online_serving/characters`

-   **Status:** BETA
-   **Display Name:** Characters
-   **Description:** Input/output character count distribution.
-   **Kind:** DELTA
-   **Value Type:** DISTRIBUTION
-   **Unit:** `1`
-   **Metric Labels:**
    -   `type`: Type of character (input/output).
    -   `request_type`: Type of request (dedicated/shared).
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.
    -   `modality`: Modality of the input/output characters.

### `publisher/online_serving/consumed_throughput`

-   **Status:** BETA
-   **Display Name:** Character Throughput
-   **Description:** Overall throughput used (accounting for burndown rate) in terms of characters.
-   **Kind:** DELTA
-   **Value Type:** INT64
-   **Unit:** `1`
-   **Metric Labels:**
    -   `request_type`: Type of request (dedicated/shared).
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.
    -   `modality`: Modality of the consumed characters.

### `publisher/online_serving/consumed_token_throughput`

-   **Status:** BETA
-   **Display Name:** Token Throughput
-   **Description:** Overall throughput used (accounting for burndown rate) in terms of tokens.
-   **Kind:** DELTA
-   **Value Type:** INT64
-   **Unit:** `1`
-   **Metric Labels:**
    -   `request_type`: Type of request (dedicated/shared).
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.
    -   `modality`: Modality of the consumed tokens.

### `publisher/online_serving/dedicated_character_limit`

-   **Status:** BETA
-   **Display Name:** Limit (characters per second)
-   **Description:** Dedicated limit in characters per second.
-   **Kind:** GAUGE
-   **Value Type:** INT64
-   **Unit:** `1/s`
-   **Metric Labels:** None

### `publisher/online_serving/dedicated_character_project_max_limit`

-   **Status:** BETA
-   **Display Name:** Project Max Limit (characters per second)
-   **Description:** Project max limit in characters per second that can be consumed.
-   **Kind:** GAUGE
-   **Value Type:** INT64
-   **Unit:** `1/s`
-   **Metric Labels:**
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.

### `publisher/online_serving/dedicated_gsu_limit`

-   **Status:** BETA
-   **Display Name:** Limit (GSU)
-   **Description:** Dedicated limit in GSU.
-   **Kind:** GAUGE
-   **Value Type:** INT64
-   **Unit:** `1`
-   **Metric Labels:** None

### `publisher/online_serving/dedicated_gsu_project_max_limit`

-   **Status:** BETA
-   **Display Name:** Project Max Limit (GSU)
-   **Description:** Project max limit in GSU that can be consumed.
-   **Kind:** GAUGE
-   **Value Type:** INT64
-   **Unit:** `1`
-   **Metric Labels:**
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.

### `publisher/online_serving/dedicated_token_limit`

-   **Status:** BETA
-   **Display Name:** Limit (tokens per second)
-   **Description:** Dedicated limit in tokens per second.
-   **Kind:** GAUGE
-   **Value Type:** INT64
-   **Unit:** `1/s`
-   **Metric Labels:** None

### `publisher/online_serving/dedicated_token_project_max_limit`

-   **Status:** BETA
-   **Display Name:** Project Max Limit (tokens per second)
-   **Description:** Project max limit in tokens per second that can be consumed.
-   **Kind:** GAUGE
-   **Value Type:** INT64
-   **Unit:** `1/s`
-   **Metric Labels:**
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.

### `publisher/online_serving/first_token_latencies`

-   **Status:** BETA
-   **Display Name:** First token latencies
-   **Description:** Duration from request received to first token sent back to the client.
-   **Kind:** DELTA
-   **Value Type:** DISTRIBUTION
-   **Unit:** `ms`
-   **Metric Labels:**
    -   `input_token_size`: The bucketized size of number of tokens in the prediction request.
    -   `output_token_size`: The bucketized size of number of tokens in the prediction response.
    -   `max_token_size`: The bucketized max size of number of tokens in the prediction request/response.
    -   `request_type`: The type of traffic of the request (dedicated/shared).
    -   `explicit_caching`: Whether the request uses explicit caching feature.

### `publisher/online_serving/model_invocation_count`

-   **Status:** BETA
-   **Display Name:** Model invocation count
-   **Description:** Number of model invocations (prediction requests).
-   **Kind:** DELTA
-   **Value Type:** INT64
-   **Unit:** `1`
-   **Metric Labels:**
    -   `input_token_size`: The bucketized size of number of tokens in the prediction request.
    -   `output_token_size`: The bucketized size of number of tokens in the prediction response.
    -   `max_token_size`: The bucketized max size of number of tokens in the prediction request/response.
    -   `response_code`: Responce code of prediction request.
    -   `request_type`: The type of traffic of the request (dedicated/shared).
    -   `method`: The type of method of the request (RawPredict/StreamRawPredict/ChatCompletions/etc).
    -   `error_category`: Response error category of the request (user/system/capacity).
    -   `explicit_caching`: Whether the request uses explicit caching feature.
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.

### `publisher/online_serving/model_invocation_latencies`

-   **Status:** BETA
-   **Display Name:** Model invocation latencies
-   **Description:** Model invocation latencies (prediction latencies).
-   **Kind:** DELTA
-   **Value Type:** DISTRIBUTION
-   **Unit:** `ms`
-   **Metric Labels:**
    -   `input_token_size`: The bucketized size of number of tokens in the prediction request.
    -   `output_token_size`: The bucketized size of number of tokens in the prediction response.
    -   `max_token_size`: The bucketized max size of number of tokens in the prediction request/response.
    -   `latency_type`: The type of latency for the prediction request (either model or overhead).
    -   `request_type`: The type of traffic of the request (dedicated/shared).
    -   `explicit_caching`: Whether the request uses explicit caching feature.

### `publisher/online_serving/token_count`

-   **Status:** BETA
-   **Display Name:** Token count
-   **Description:** Accumulated input/output token count.
-   **Kind:** DELTA
-   **Value Type:** INT64
-   **Unit:** `1`
-   **Metric Labels:**
    -   `max_token_size`: The bucketized max size of number of tokens in the prediction request/response.
    -   `type`: Type of token (input/output).
    -   `request_type`: The type of traffic of the request (dedicated/shared).
    -   `explicit_caching`: Whether the request uses explicit caching feature.
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.
    -   `modality`: Modality of the input/output tokens.
    -   `source`: The source/surface that the token consumption is originated from. For global endpoint, this is 'global'; otherwise, this is the region where a request is served. The label can also have prefix, such as 'batch_', to indicate product breakdown.

### `publisher/online_serving/tokens`

-   **Status:** BETA
-   **Display Name:** Tokens
-   **Description:** Input/output token count distribution.
-   **Kind:** DELTA
-   **Value Type:** DISTRIBUTION
-   **Unit:** `1`
-   **Metric Labels:**
    -   `max_token_size`: The bucketized max size of number of tokens in the prediction request/response.
    -   `type`: Type of token (input/output).
    -   `request_type`: The type of traffic of the request (dedicated/shared).
    -   `accounting_resource`: The identifier of the GCP project/folder/org to which quota is accounted to. Available for Provisioned Throughput only.
    -   `modality`: Modality of the input/output tokens.
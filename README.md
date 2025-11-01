# Google Cloud AI Platform Metrics Monitor

A command-line tool to query and visualize daily usage and performance metrics for Google Cloud's Vertex AI Platform models.

This script queries the Google Cloud Monitoring API to fetch metrics, display the data in various formats, and generate time-series charts for analysis.

## Features

*   **Comprehensive Metric Querying:**
    *   Query a wide range of pre-configured metrics (e.g., token throughput, invocation counts, latencies).
    *   Query a single metric or all available metrics at once.
*   **Powerful Chart Generation:**
    *   Generate time-series line charts for any single metric.
    *   Create multi-line charts by grouping data by one or more dimensions (e.g., `model_user_id`, `request_type`).
    *   Generate a standardized report of 6 key charts with a single command.
*   **Flexible and Secure:**
    *   Specify custom time ranges for queries.
    *   Output data in Markdown, CSV, or JSON.
    *   Uses Application Default Credentials (ADC) for secure authentication.
    *   Logs the authentication method (User vs. Service Account) on startup.
*   **Robust and Extensible:**
    *   Organized into a clean Python package structure.
    *   Uses Pydantic for type-safe and validated metric configurations.
    *   Separation of concerns between the GCP client, charting logic, and configuration makes it easy to extend.

## Prerequisites

*   Python 3.9+
*   `uv` (Python package installer and dependency manager)
*   Access to a Google Cloud project.
*   The **AI Platform (Vertex AI) API** and **Cloud Monitoring API** must be enabled for your project.
*   The `gcloud` CLI installed and configured on your machine.

## Setup

### 1. Install Dependencies

The required Python packages are listed in `pyproject.toml`. Install them using `uv`:

```bash
uv pip install
```

## Authentication and Authorization

This tool uses Google's **Application Default Credentials (ADC)** system. The script automatically detects and uses credentials based on your environment, requiring no code changes.

### Method 1: User Credentials (for Local Development)

1.  **Log in with gcloud:**
    ```bash
    gcloud auth application-default login
    ```
2.  **Set your project:**
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

### Method 2: Service Account (for Automation & Production)

1.  **Create a Service Account** in the GCP Console.
2.  **Grant Permissions:** Assign the **"Monitoring Viewer"** IAM role to the service account.
3.  **Create and Download a JSON Key** for the service account.
4.  **Set the Environment Variable:** Point the following environment variable to the path of your downloaded key file.

    - **On Linux or macOS:**
      ```bash
      export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
      ```
    - **On Windows (PowerShell):**
      ```powershell
      $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
      ```

## Running the Script

Because the project is structured as a Python package, you must run it as a module from the project's root directory.

### Basic Usage

*   **Query a single metric:**
    ```bash
    uv run python -m monitor.main --project-id YOUR_PROJECT_ID --metric consumed_token_throughput
    ```*   **Query all metrics:**
    ```bash
    uv run python -m monitor.main --project-id YOUR_PROJECT_ID --all-metrics
    ```
### Chart Generation Examples

*   **Generate a standard report of 6 key charts:**
    ```bash
    uv run python -m monitor.main --project-id YOUR_PROJECT_ID --generate-report-charts
    ```*   **Generate a report filtered by a specific model:**
    ```bash
    uv run python -m monitor.main --project-id YOUR_PROJECT_ID --generate-report-charts --filter-model-id gemini-1.5-pro
    ```*   **Generate a custom chart for a single metric, grouped by model:**
    ```bash
    uv run python -m monitor.main --project-id YOUR_PROJECT_ID --metric consumed_token_throughput --generate-graph --graph-group-by model_user_id
    ```
### Command-Line Arguments

| Argument                     | Description                                                                                             | Used With                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| `--project-id`               | **(Required)** Your Google Cloud Project ID.                                                            | All modes                               |
| `--metric`                   | Query a single metric for data output.                                                                  | Mutually exclusive mode                 |
| `--all-metrics`              | Query all available metrics sequentially for data output.                                               | Mutually exclusive mode                 |
| `--generate-report-charts`   | Generate a standard set of charts for key metrics.                                                      | Mutually exclusive mode                 |
| `--days-ago-start`           | The start of the time window in days from now. Default: `90`.                                           | All modes                               |
| `--days-ago-end`             | The end of the time window in days from now (0 is 'now'). Default: `0`.                                 | All modes                               |
| `--output`                   | The output format for the results (`markdown`, `csv`, `json`). Default: `markdown`.                     | `--metric`, `--all-metrics`             |
| `--generate-graph`           | Generate a chart for the queried metric.                                                                | `--metric`                              |
| `--graph-group-by`           | Comma-separated columns to group by for the chart (e.g., `model_user_id,request_type`).                 | `--generate-graph`                      |
| `--filter-model-id`          | Filter the data by a specific `model_user_id` before generating charts.                                 | `--generate-report-charts`              |

*Note: You must specify exactly one of `--metric`, `--all-metrics`, or `--generate-report-charts`.*

### Available Metrics

You can find a full list of available metrics in `monitor/config/metrics.py`.

## Sample Output

See [`docs/sample.md`](./docs/sample.md) for an example of the output when running with the `--all-metrics` flag.

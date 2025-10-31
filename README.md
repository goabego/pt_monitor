# Google Cloud AI Platform Metrics Monitor

This script (`monitor.py`) queries the Google Cloud Monitoring API to fetch and display daily usage and performance metrics for AI Platform models. It is a command-line tool that allows you to query various metrics, aggregate the data by day, and output the results in different formats.

## Features

*   **Multiple Metrics:** Query a wide range of metrics, including token throughput, invocation counts, latencies, and more.
*   **Flexible Time Ranges:** Specify custom time ranges for your queries.
*   **Multiple Output Formats:** Get your data in Markdown, CSV, or JSON format.
*   **Robust and Extensible:** The codebase is structured with best practices, making it easy to add new metric configurations.

## Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)
*   Access to a Google Cloud project.
*   The **AI Platform (Vertex AI) API** and **Cloud Monitoring API** must be enabled for your project.
*   The `gcloud` CLI installed and configured on your machine.

## Setup

### 1. Create a Virtual Environment

It is highly recommended to use a virtual environment to keep dependencies isolated.

```bash
# For Linux and macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

The required Python packages are listed in `requirements.txt`. Install them using `pip`:

```bash
pip install -r requirements.txt
```

This will install the following libraries:
*   `google-cloud-monitoring`: The client library for the Google Cloud Monitoring API.
*   `pandas`: For data manipulation and creating the DataFrame.
*   `tabulate`: Used by pandas to generate the markdown-formatted table.

### 3. Google Cloud Authentication

This script uses Application Default Credentials (ADC) to authenticate with Google Cloud. The easiest way to set this up for local development is with the `gcloud` CLI.

1.  **Log in with gcloud:**
    ```bash
    gcloud auth application-default login
    ```
    This command will open a browser window for you to log in and grant the necessary permissions.

2.  **Set your project:**
    Make sure your `gcloud` CLI is configured to use the correct project.
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

3.  **Permissions:**
    Ensure the account you authenticated with has the **"Monitoring Viewer"** IAM role (or a custom role with the `monitoring.timeSeries.list` permission) on the target project.

## Running the Script

The script is run from the command line and accepts several arguments to customize the query.

### Basic Usage

To query a specific metric, you must provide your project ID and the metric name.

```bash
python monitor.py --project-id YOUR_PROJECT_ID --metric consumed_token_throughput
```

### Query All Metrics

You can query all available metrics sequentially using the `--all-metrics` flag.

```bash
python monitor.py --project-id YOUR_PROJECT_ID --all-metrics
```

### Command-Line Arguments

| Argument           | Required | Description                                                                  |
| ------------------ | -------- | ---------------------------------------------------------------------------- |
| `--project-id`     | **Yes**  | Your Google Cloud Project ID.                                                |
| `--metric`         | **Yes*** | The metric to query (e.g., `consumed_token_throughput`).                     |
| `--all-metrics`    | **Yes*** | Query all available metrics sequentially.                                    |
| `--days-ago-start` | No       | The start of the time window in days from now. Default: `90`.                |
| `--days-ago-end`   | No       | The end of the time window in days from now (0 is 'now'). Default: `0`.      |
| `--output`         | No       | The output format for the results (`markdown`, `csv`, `json`). Default: `markdown`. |

*\*Note: You must specify either `--metric` or `--all-metrics`, but not both.*

### Available Metrics

You can find a full list of available metrics in the `METRIC_CONFIGS` dictionary inside the `metric_configs.py` file.

## Sample Output

The output is a table showing the daily data for the requested metric, broken down by relevant labels.

See [`sample.md`](./sample.md) for a more detailed example of the output when running with the `--all-metrics` flag.
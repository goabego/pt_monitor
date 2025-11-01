# Google Cloud AI Platform Metrics Monitor

This script (`monitor.py`) queries the Google Cloud Monitoring API to fetch and display daily usage and performance metrics for AI Platform models. It is a command-line tool that allows you to query various metrics, aggregate the data by day, and output the results in different formats.

## Features

*   **Multiple Metrics:** Query a wide range of metrics, including token throughput, invocation counts, latencies, and more.
*   **Flexible Time Ranges:** Specify custom time ranges for your queries.
*   **Multiple Output Formats:** Get your data in Markdown, CSV, or JSON format.
*   **Robust and Extensible:** The codebase is structured with best practices, making it easy to add new metric configurations.
*   **Authentication Awareness:** The script logs the authentication method being used (User Credentials vs. Service Account) on startup.

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

## Authentication and Authorization

### How it Works: Application Default Credentials (ADC)

This script uses the **Application Default Credentials (ADC)** strategy provided by Google Cloud. This means the code itself does not handle credentials; instead, the Google Cloud client library automatically finds the credentials based on the environment where the script is running.

This approach separates credential management from the code, making it more secure and flexible. The script will automatically detect and use one of the two primary authentication methods described below.

### Authentication Methods

You can use either your own user account (ideal for local development) or a dedicated service account (best for automated environments).

#### Method 1: User Credentials (for Local Development)

This is the quickest way to get started for testing on your local machine.

1.  **Log in with gcloud:**
    Run the following command in your terminal. It will open a browser window for you to log in to your Google account.
    ```bash
    gcloud auth application-default login
    ```

2.  **Set your project:**
    Make sure your `gcloud` CLI is configured to use the correct project.
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```
    When you run the script, it will log that it is using "User Credentials".

#### Method 2: Service Account (for Automation & Production)

A service account is a special type of Google account intended to represent a non-human user that needs to authenticate and be authorized to access data in Google APIs. This is the recommended method for any automated workflow.

1.  **Create a Service Account:**
    - Go to the [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts) in the Google Cloud Console.
    - Select your project.
    - Click **"+ CREATE SERVICE ACCOUNT"**.
    - Give it a name (e.g., `metrics-monitor`) and an optional description.
    - Click **"CREATE AND CONTINUE"**.

2.  **Grant Permissions:**
    - In the "Grant this service account access to project" step, click the **"Role"** dropdown.
    - Select **"Monitoring Viewer"**. This role grants the necessary permission (`monitoring.timeSeries.list`) to read metric data.
    - Click **"CONTINUE"**, then **"DONE"**.

3.  **Create a JSON Key:**
    - Find the service account you just created in the list.
    - Click the three-dot menu (Actions) on the right and select **"Manage keys"**.
    - Click **"ADD KEY"** -> **"Create new key"**.
    - Select JSON as the key type and click **"CREATE"**.
    - A JSON key file will be downloaded to your computer. **Treat this file as a secret.**

4.  **Set the Environment Variable:**
    The client library will automatically find the key if you set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the downloaded JSON file.

    - **On Linux or macOS:**
      ```bash
      export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
      ```
    - **On Windows (PowerShell):**
      ```powershell
      $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
      ```
    When you run the script from a terminal where this variable is set, it will log that it is using a "Service Account" and will show the service account's email.

## Running the Script

Because the project is structured as a Python package, you must run it as a module from the root directory of the project.

### Basic Usage

To query a specific metric, provide your project ID and the metric name:

```bash
python -m monitor.main --project-id YOUR_PROJECT_ID --metric consumed_token_throughput
```

### Query All Metrics

To query all available metrics sequentially, use the `--all-metrics` flag:

```bash
python -m monitor.main --project-id YOUR_PROJECT_ID --all-metrics
```

### Generating Charts

To generate a chart for a single metric, use the `--generate-graph` flag. You can also specify one or more columns to group the data by.

```bash
# Generate a time-series chart for 'consumed_token_throughput' grouped by 'model_user_id'
python -m monitor.main --project-id YOUR_PROJECT_ID --metric consumed_token_throughput --generate-graph --graph-group-by model_user_id
```

To generate the standard report of 6 charts, use the `--generate-report-charts` flag:
```bash
python -m monitor.main --project-id YOUR_PROJECT_ID --generate-report-charts
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

*Note: You must specify either `--metric` or `--all-metrics`, but not both.*

### Available Metrics

You can find a full list of available metrics in the `METRIC_CONFIGS` dictionary inside the `metric_configs.py` file.

## Sample Output

The output is a table showing the daily data for the requested metric, broken down by relevant labels.

See [`sample.md`](./sample.md) for a more detailed example of the output when running with the `--all-metrics` flag.

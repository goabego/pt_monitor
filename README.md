# Google Cloud AI Platform Token Usage Monitor

This script (`monitor.py`) queries the Google Cloud Monitoring API to fetch and display the daily consumed token throughput for AI Platform models. It aggregates the data by day, project, location, endpoint, deployed model, and request type, then prints a summary table to the console.

## Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)
*   Access to a Google Cloud project.
*   The **AI Platform (Vertex AI) API** and **Cloud Monitoring API** must be enabled for your project.
*   The `gcloud` CLI installed and configured on your machine.

## Setup

Follow these steps to set up your environment and run the script.

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

The required Python packages are listed in `requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```

This will install the following libraries:
*   `google-cloud-monitoring`: The client library for the Google Cloud Monitoring API.
*   `pandas`: For data manipulation and creating the DataFrame.
*   `tabulate`: Used by pandas to generate the markdown-formatted table for printing.

### 3. Google Cloud Authentication

This script uses Application Default Credentials (ADC) to authenticate with Google Cloud. The easiest way to set this up for local development is to use the `gcloud` CLI.

1.  **Log in with gcloud:**

    ```bash
    gcloud auth application-default login
    ```

    This command will open a browser window for you to log in to your Google account and grant the necessary permissions.

2.  **Set your project:**
    Make sure your gcloud CLI is configured to use the correct project.
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

3.  **Permissions:**
    Ensure the account you authenticated with has the **"Monitoring Viewer"** IAM role (or a custom role with the `monitoring.timeSeries.list` permission) on the target project.

## Running the Script

### 1. Configure the Project ID

Before running, you must edit `monitor.py` and set the `PROJECT_ID` variable to your Google Cloud project ID.

Find this line near the bottom of the script:
```python
# /home/admin_/monitor.py

PROJECT_ID = "agent-starter-pack-spend" 
```

Replace `"agent-starter-pack-spend"` with your actual project ID.

### 2. Execute the Script

With your virtual environment activated, run the script from your terminal:

```bash
python monitor.py
```

The script will print the status of the query and then display a markdown table with the daily token usage data.

## Output

The output is a table showing the daily consumed tokens, broken down by date, project, location, endpoint, deployed model, and request type.

Example:
```
| date       | resource_container       | location    | endpoint_id   | deployed_model_id   | request_type   |   consumed_tokens |
|:-----------|:-------------------------|:------------|:--------------|:--------------------|:---------------|------------------:|
| 2025-08-04 | my-gcp-project           | us-central1 | 123456789...  | 987654321...        | shared         |             28133 |
...
```

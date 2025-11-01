import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generate_chart(df: pd.DataFrame, metric_name: str, value_column: str, group_by: list = None):
    """
    Generates and saves a time-series line chart from the metric data.
    If group_by columns are provided, it plots a separate line for each category combination.
    """
    if df.empty:
        logging.warning(f"No data available to generate a chart for {metric_name}.")
        return

    plt.figure(figsize=(14, 8))
    
    # Ensure date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    title = f'Daily {metric_name} Over Time'

    # Check for valid grouping columns
    valid_group_by = [col for col in group_by if col in df.columns] if group_by else []

    if not valid_group_by:
        # Plot a single line for the total value over time
        time_series_data = df.groupby('date')[value_column].sum()
        time_series_data.plot(kind='line', marker='o', linestyle='-')
    else:
        # Create a pivot table for plotting multiple lines
        pivot_df = df.groupby(['date'] + valid_group_by)[value_column].sum()
        
        try:
            # Unstack the grouping columns to create separate columns for each category
            plot_df = pivot_df.unstack(level=valid_group_by)
            plot_df.plot(kind='line', marker='o', linestyle='-')
            
            group_by_str = ' & '.join(valid_group_by)
            title += f' by {group_by_str}'
            plt.legend(title=group_by_str, bbox_to_anchor=(1.05, 1), loc='upper left')
        except Exception as e:
            logging.error(f"Could not generate multi-line chart, possibly due to data structure: {e}")
            logging.info("Falling back to a single total line chart.")
            time_series_data = df.groupby('date')[value_column].sum()
            time_series_data.plot(kind='line', marker='o', linestyle='-')

    plt.title(title)
    plt.ylabel(f'Total {value_column}')
    plt.xlabel('Date')
    plt.grid(True)
    plt.tight_layout()
    
    filename = f"{metric_name}_chart.png"
    plt.savefig(filename)
    logging.info(f"Chart saved to {filename}")
    plt.close()
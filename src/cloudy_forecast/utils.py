import json
import sys
from pathlib import Path
import pandas as pd
import datetime

# Define the relative path to your config
CONFIG_PATH = Path.home() / ".cloudy_forecast.json"
RAW_DATA_PATH = "data/raw/"


def load_config() -> dict:
    """Loads configuration and validates contents."""
    if not CONFIG_PATH.exists():
        print(f"Error: Configuration file not found at {CONFIG_PATH}")
        sys.exit(1)

    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {CONFIG_PATH} contains invalid JSON.")
        sys.exit(1)

    # Validation logic
    cities = config.get("cities", {})
    metrics = config.get("metrics", [])

    if not cities:
        print("Error: No cities defined in config.json.")
        sys.exit(1)

    if not metrics:
        print("Error: No metrics defined in config.json.")
        sys.exit(1)

    return config


def store_forecast(city: str = None, data: pd.DataFrame = None) -> None:
    """Store raw forecasting data
    
    Args:
        data (pandas.DataFrame): DataFrame containing the forecasting data
    
    Returns:
        None
    """
    if city is None:
        print("No city name was passed.")
        return None
    elif data is None:
        print("No data was passed.")
        return None
    else:
        # check today's date
        today = datetime.date.today()
        today_str = today.strftime("%Y%m%d")
        file_name = f"{today_str}_{city}.csv"
        data.to_csv(f"{RAW_DATA_PATH}/{file_name}", index=False)
        print("Successfully stored today's forecasting data.")

"""
navigate to ~/code/uni/sce/cloudy_forecast
activate python environment
execute uv run cloudy_forecast download

"""
"""Forecast class for managing weather forecast data and error estimation."""

import numpy as np
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from .utils import store_forecast


class Forecast:
    """Class to manage weather forecasts and compute error estimates over time."""

    def __init__(self) -> None:
        """Initialize a new Forecast instance."""
        self.city: str | None = None
        self.latitude: float | None = None
        self.longitude: float | None = None
        self.parameters: list[str] = []
        self.current_forecast: pd.DataFrame | None = None
        self.historical_data: list[pd.DataFrame] = []  # Store past forecasts

    def set_location(self, city: str, lat: float, long: float) -> None:
        """Set the location for the forecast.

        Args:
            city: Name of the location.
            lat: Latitude of the location.
            long: Longitude of the location.
        """
        self.city = city
        self.latitude = lat
        self.longitude = long

    def set_parameters(self, parameters: list[str]) -> None:
        """Set the weather parameters to forecast.

        Args:
            parameters: List of parameter names (e.g., ["temperature_2m_max", "temperature_2m_min"]).
        """
        self.parameters = parameters

    def download(self) -> str:  # type: ignore[no-untyped-def]
        """Download the current forecast for the set location and parameters."""
        # Validate that location and parameters are set
        if self.latitude is None or self.longitude is None:
            raise ValueError("Location not set. Call set_location() first.")
        if not self.parameters:
            raise ValueError("Parameters not set. Call set_parameters() first.")

        # 1. Setup API Client
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)  # type: ignore

        # 2. Prepare API Call
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "daily": self.parameters,
            "timezone": "auto",  # Aligns daily buckets to local midnight
        }

        try:
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
        except Exception as e:
            return f"Error fetching forecast: {e}"

        # 3. Dynamic Data Extraction
        daily = response.Daily()

        # Generate UTC date range from the API response
        utc_dates = pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),  # type: ignore
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),  # type: ignore
            freq=pd.Timedelta(seconds=daily.Interval()),  # type: ignore
            inclusive="left",
        )

        # Convert UTC to local time (Europe/Berlin) and extract only the date component
        # This shifts '22:00 UTC' to '00:00 Local' and removes the time/offset
        local_dates = utc_dates.tz_convert("Europe/Berlin").date

        # Create base dictionary with formatted local dates
        daily_data: dict[str, Any] = {
            "date": local_dates
        }

        # Loop through requested parameters and extract values by index
        for i, var_name in enumerate(self.parameters):
            daily_data[var_name] = daily.Variables(i).ValuesAsNumpy()  # type: ignore

        # 4. Store and Return
        self.current_forecast = pd.DataFrame(data=daily_data)
        
        # Ensure self.city is defined in your __init__ or passed here
        store_forecast(city=self.city, data=self.current_forecast)

        return "Forecast successfully downloaded and stored."

  

    def compute_errors(self) -> str:
        """Compute error estimates based on historical forecast data."""
        return "Hello from compute_errors()"

    def show(self) -> str:
        """Display the current forecast with estimated errors."""
        print(self.current_forecast)
        return "Hello from show()"

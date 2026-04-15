"""Forecast class for managing weather forecast data and error estimation."""

from typing import Any

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
        # Validate that location, parameters, and city are set
        if self.latitude is None or self.longitude is None or self.city is None:
            raise ValueError("Location or city not set. Call set_location() first.")
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

        # Get the UTC offset provided by the API for the current location
        offset_seconds = response.UtcOffsetSeconds()
        offset_delta = pd.Timedelta(seconds=offset_seconds)

        # Generate the UTC date range
        utc_dates = pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),  # type: ignore
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),  # type: ignore
            freq=pd.Timedelta(seconds=daily.Interval()),  # type: ignore
            inclusive="left",
        )

        # Shift dates by the offset and format as strings to prevent UTC reversion in CSV
        # This resolves the "22:00 UTC" issue and satisfies static analysis
        local_date_strings = (utc_dates + offset_delta).strftime("%Y-%m-%d")

        # Create base dictionary using the formatted strings
        daily_data: dict[str, Any] = {"date": local_date_strings}

        # Loop through requested parameters and extract values by index
        for i, var_name in enumerate(self.parameters):
            daily_data[var_name] = daily.Variables(i).ValuesAsNumpy()  # type: ignore

        # 4. Store and Return
        self.current_forecast = pd.DataFrame(data=daily_data)

        # self.city is guaranteed to be a string here due to the check at the top
        store_forecast(city=self.city, data=self.current_forecast)

        return "Forecast successfully downloaded and stored."

    def compute_errors(self) -> str:
        """Compute error estimates based on historical forecast data."""
        return "Hello from compute_errors()"

    def show(self) -> str:
        """Display the current forecast with estimated errors."""
        print(self.current_forecast)
        return "Hello from show()"

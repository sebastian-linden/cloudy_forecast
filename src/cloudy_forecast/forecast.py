"""Forecast class for managing weather forecast data and error estimation."""

import pandas as pd


class Forecast:
    """Class to manage weather forecasts and compute error estimates over time."""

    def __init__(self) -> None:
        """Initialize a new Forecast instance."""
        self.latitude: float | None = None
        self.longitude: float | None = None
        self.parameters: list[str] = []
        self.current_forecast: pd.DataFrame | None = None
        self.historical_data: list[pd.DataFrame] = []  # Store past forecasts

    def set_location(self, lat: float, long: float) -> None:
        """Set the location for the forecast.

        Args:
            lat: Latitude of the location.
            long: Longitude of the location.
        """
        print("Hello from set_location()")
        self.latitude = lat
        self.longitude = long

    def set_parameters(self, params: list[str]) -> None:
        """Set the weather parameters to forecast.

        Args:
            params: List of parameter names (e.g., ["temperature_2m_max", "temperature_2m_min"]).
        """
        print("Hello from set_parameters()")
        self.parameters = params

    def download(self) -> str:
        """Download the current forecast for the set location and parameters."""
        return "Hello from download()"

    def save(self) -> None:
        """Save the current forecast data, accumulating historical data."""
        print("Hello from save()")

    def compute_errors(self) -> None:
        """Compute error estimates based on historical forecast data."""
        print("Hello from compute_errors()")

    def show(self) -> None:
        """Display the current forecast with estimated errors."""
        print("Hello from show()")

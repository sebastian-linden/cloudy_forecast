"""Tests for `cloudy_forecast` package."""

import cloudy_forecast


def test_import():
    """Verify the package can be imported."""
    assert cloudy_forecast


def test_forecast():
    """Verify correct import of my own code"""
    forecast = cloudy_forecast.Forecast()

    # Test set_location
    forecast.set_location(lat=50, long=6)
    assert forecast.latitude == 50
    assert forecast.longitude == 6

    # Test set_parameters
    params = ["temperature_2m_max", "temperature_2m_min"]
    forecast.set_parameters(params)
    assert forecast.parameters == params

    # Test download
    assert forecast.download() == "Hello from download()"

    # Test save
    forecast.save()

    # Test compute_errors
    forecast.compute_errors()

    # Test show
    forecast.show()

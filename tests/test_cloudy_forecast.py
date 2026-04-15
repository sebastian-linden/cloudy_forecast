"""Tests for `cloudy_forecast` package."""

import cloudy_forecast


def test_import():
    """Verify the package can be imported."""
    assert cloudy_forecast


def test_forecast_init():
    """Verify the correct initialization of a forecast object"""
    assert cloudy_forecast.Forecast()


def test_forecast_set_location():
    """Test whether setting the location works."""
    forecast = cloudy_forecast.Forecast()
    # Test set_location
    forecast.set_location(lat=50, long=6)
    assert forecast.latitude == 50
    assert forecast.longitude == 6


def test_forecast_set_parameters():
    """Test whether specifying the parameters works."""
    forecast = cloudy_forecast.Forecast()
    # Test set_parameters
    params = ["temperature_2m_max", "temperature_2m_min"]
    forecast.set_parameters(params)
    assert forecast.parameters == params


def test_forecast_download():
    """Test download function."""
    forecast = cloudy_forecast.Forecast()

    # Must set location and parameters before downloading
    forecast.set_location(lat=50, long=6)
    forecast.set_parameters(["temperature_2m_max", "temperature_2m_min"])

    # Test download
    result = forecast.download()
    assert "successfully" in result.lower() or "downloaded" in result.lower()


def test_forecast_compute_errors():
    """Test download function."""
    forecast = cloudy_forecast.Forecast()

    # Test download
    assert forecast.compute_errors() == "Hello from compute_errors()"


def test_forecast_show():
    """Test download function."""
    forecast = cloudy_forecast.Forecast()

    # Test download
    assert forecast.show() == "Hello from show()"

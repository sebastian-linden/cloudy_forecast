"""Console script for cloudy_forecast."""

import typer

from .utils import load_config

app = typer.Typer()


@app.command()
def help() -> None:
    help_message = """
    [Placeholder help message]
    """
    print(help_message)
    return None


@app.command()
def download() -> None:
    """Initiates download using settings from data/config.json."""

    # Read configuration file
    config = load_config()
    cities = config["cities"]
    weather_metrics = config["metrics"]

    # Initiate forecast object
    from .forecast import Forecast

    fc = Forecast()

    # set location -> For now just Aachen
    city = "aachen"
    ac_lat = cities[city]["lat"]
    ac_lon = cities[city]["lon"]
    fc.set_location(city=city,lat=ac_lat, long=ac_lon)

    # set parameters
    fc.set_parameters(parameters=weather_metrics)

    # download forecast data
    fc.download()

    # # Iterating through the validated data
    # for city_name, coords in cities.items():
    #     print(f"Fetching data for {city_name}...")
    #     # forecast = Forecast(lat=coords['lat'], lon=coords['lon'], metrics=metrics)

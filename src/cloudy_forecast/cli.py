"""Console script for cloudy_forecast."""

from typing import Annotated

import typer

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
    from .utils import load_config

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
    fc.set_location(city=city, lat=ac_lat, long=ac_lon)

    # set parameters
    fc.set_parameters(parameters=weather_metrics)

    # download forecast data
    fc.download()

    # # Iterating through the validated data
    # for city_name, coords in cities.items():
    #     print(f"Fetching data for {city_name}...")
    #     # forecast = Forecast(lat=coords['lat'], lon=coords['lon'], metrics=metrics)


@app.command()
def schedule(action: Annotated[str, typer.Argument(help="Either 'activate' or 'deactivate'")]) -> None:
    from .utils import set_schedule

    """Automates the setup or removal of the systemd timer."""

    set_schedule(action=action)

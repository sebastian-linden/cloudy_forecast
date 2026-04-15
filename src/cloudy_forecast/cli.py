"""Console script for cloudy_forecast."""

import typer
from rich.console import Console

from cloudy_forecast import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for cloudy_forecast."""
    console.print("Replace this message by putting your code into cloudy_forecast.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()

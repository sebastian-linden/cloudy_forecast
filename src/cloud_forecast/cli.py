"""Console script for cloud_forecast."""

import typer
from rich.console import Console

from cloud_forecast import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for cloud_forecast."""
    console.print("Replace this message by putting your code into cloud_forecast.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()

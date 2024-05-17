from typing import Optional

import typer
from typing_extensions import Annotated

from libyear.__about__ import __version__
from libyear.results import OutputFormat, calculate_results
from libyear.toml import load_requirements_from_toml
from libyear.utils import (
    load_requirements,
)

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"libyear version: {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    """
    A simple measure of software dependency freshness.
    """
    ...


@app.command()
def text(
    requirements_file: Annotated[
        str, typer.Argument(help="requirements.txt file path")
    ],
    json: Annotated[bool, typer.Option(help="Write the output as JSON")] = False,
    sort: Annotated[
        bool, typer.Option(help="Sort by years behind, in descending order")
    ] = False,
):
    """
    The text command reads a requirements.txt file and prints a table with the
    libyear calculations.
    """
    loaded_requirements = load_requirements(requirements_file)
    requirements = set()
    requirements.update(loaded_requirements)
    if json:
        calculate_results(requirements, sort, OutputFormat.JSON)
    else:
        calculate_results(requirements, sort)


@app.command()
def toml(
    pyproject: Annotated[str, typer.Argument(help="pyproject.toml path")],
    json: Annotated[bool, typer.Option(help="Write the output as JSON")] = False,
    sort: Annotated[
        bool, typer.Option(help="Sort by years behind, in descending order")
    ] = False,
):
    """
    The toml command reads a pyproject.toml file and prints a table with the
    libyear calculations.
    """
    loaded_requirements = load_requirements_from_toml(pyproject)
    requirements = set()
    requirements.update(loaded_requirements)

    if json:
        calculate_results(requirements, sort, OutputFormat.JSON)
    else:
        calculate_results(requirements, sort)


if __name__ == "__main__":
    app()

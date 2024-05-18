from typing import Optional

import typer
from typing_extensions import Annotated

from libyear.__about__ import __version__
from libyear.results import (
    calculate_results,
    results_to_json,
    results_to_stdout,
)
from libyear.toml import load_requirements_from_toml
from libyear.utils import (
    load_requirements,
    validate_file_path,
)

app = typer.Typer()


def version_callback(value: bool):
    """
    Print the version of the application
    """
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
    json: Annotated[
        str, typer.Option(help="Write the output as JSON to the given file")
    ] = "",
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

    render_results(json, sort, requirements)


@app.command()
def toml(
    pyproject: Annotated[str, typer.Argument(help="pyproject.toml path")],
    json: Annotated[
        str, typer.Option(help="Write the output as JSON to the given file")
    ] = "",
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

    render_results(json, sort, requirements)


def render_results(json: str, sort: bool, requirements: set) -> None:
    """
    Render the results to the console or to a file
    """
    if json:
        validate_file_path(json)
    data = calculate_results(requirements, sort)
    if json:
        results_to_json(data=data, file_name=json)
    else:
        results_to_stdout(data=data)


if __name__ == "__main__":
    app()

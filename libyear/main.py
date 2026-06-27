import asyncio
from importlib.metadata import version
from typing import Optional

import typer
from httpx import AsyncClient
from typing_extensions import Annotated

__version__ = version("pylibyear")
from libyear.results import (
    Results,
    calculate_results,
    results_to_json,
    results_to_stdout,
)
from libyear.toml import load_requirements_from_toml
from libyear.utils import load_requirements

app = typer.Typer()

client = AsyncClient(http2=True)


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
    fail_over: Annotated[int, typer.Option(help="Fail over a certain age")] = 0,
):
    """
    The text command reads a requirements.txt file and prints a table with the
    libyear calculations.
    """
    loaded_requirements = load_requirements(requirements_file)
    requirements = set()
    requirements.update(loaded_requirements)

    data = render_results(json, sort, requirements)
    if fail_over and data.total_years > fail_over:
        raise typer.Exit(code=1)


@app.command()
def toml(
    pyproject: Annotated[str, typer.Argument(help="pyproject.toml path")],
    json: Annotated[
        str, typer.Option(help="Write the output as JSON to the given file")
    ] = "",
    sort: Annotated[
        bool, typer.Option(help="Sort by years behind, in descending order")
    ] = False,
    fail_over: Annotated[int, typer.Option(help="Fail over a certain age")] = 0,
):
    """
    The toml command reads a pyproject.toml file and prints a table with the
    libyear calculations.
    """
    loaded_requirements = load_requirements_from_toml(pyproject)
    requirements = set()
    requirements.update(loaded_requirements)

    data = render_results(json, sort, requirements)
    if fail_over and data.total_years > fail_over:
        raise typer.Exit(code=1)


def render_results(json: str, sort: bool, requirements: set) -> Results:
    """
    Render the results to the console or to a file
    """
    data = asyncio.run(calculate_results(requirements, sort))
    if json:
        results_to_json(data=data, file_name=json)
    else:
        results_to_stdout(data=data)

    return data


if __name__ == "__main__":
    app()

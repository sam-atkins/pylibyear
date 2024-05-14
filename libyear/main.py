import typer
from typing_extensions import Annotated

from libyear.results import print_results_table
from libyear.toml import load_requirements_from_toml
from libyear.utils import (
    load_requirements,
)

app = typer.Typer()


@app.command()
def text(
    requirements_file: Annotated[
        str, typer.Argument(help="requirements.txt file path")
    ],
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
    print_results_table(requirements, sort)


@app.command()
def toml(
    pyproject: Annotated[str, typer.Argument(help="pyproject.toml path")],
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
    print_results_table(requirements, sort)


if __name__ == "__main__":
    app()

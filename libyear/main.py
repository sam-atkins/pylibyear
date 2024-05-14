import typer
from prettytable import PrettyTable
from typing_extensions import Annotated

from libyear.pypi import get_lib_days
from libyear.utils import (
    get_requirement_name_and_version,
    load_requirements,
)

app = typer.Typer()


@app.command()
def text(
    requirements_file: Annotated[
        str, typer.Argument(help="Requirements.txt file(s) path")
    ],
    sort: Annotated[
        bool, typer.Option(help="Sort by years behind, in descending order")
    ] = False,
):
    requirements = set()

    requirements.update(load_requirements(requirements_file))

    pt = PrettyTable()
    pt.field_names = ["Library", "Current Version", "Latest Version", "Libyears behind"]
    total_days = 0

    for req in requirements:
        name, version, version_lt = get_requirement_name_and_version(req)
        if not name:
            continue

        if not version and not version_lt:
            continue

        v, lv, days = get_lib_days(name, version, version_lt)
        if v and days > 0:
            pt.add_row([name, v, lv, str(round(days / 365, 2))])
        total_days += days

    if sort:
        pt.sortby = "Libyears behind"
        pt.reversesort = True

    if total_days == 0:
        print("Your system is up-to-date!")
    else:
        print(pt)
        print("Your system is %s libyears behind" % str(round(total_days / 365, 2)))


if __name__ == "__main__":
    app()

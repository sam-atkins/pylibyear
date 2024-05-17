import json
import sys
from enum import Enum

from prettytable import PrettyTable

from libyear.pypi import get_lib_days
from libyear.utils import get_requirement_name_and_version


class OutputFormat(Enum):
    STDOUT = "STDOUT"
    JSON = "JSON"


def calculate_results(
    requirements: set,
    sort: bool = False,
    output_fmt: OutputFormat = OutputFormat.STDOUT,
):
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

    total_days = str(round(total_days / 365, 2))

    if output_fmt == OutputFormat.JSON:
        _results_to_json(pt, total_days)
        sys.exit(0)

    _results_to_stdout(pt, total_days)


def _results_to_stdout(pt: PrettyTable, total_days: str):
    if total_days == 0:
        print("Your system is up-to-date!")
    else:
        print(pt)
        print(f"Your system is {total_days} libyears behind")


def _results_to_json(pt: PrettyTable, total_days: str):
    """
    Prepare the results in JSON format and write to a file
    """
    table = _prepare_data_for_file_output(pt, total_days)
    result = json.dumps(table, indent=4)
    print(result)
    _write_to_json_file(result)


def _prepare_data_for_file_output(pt: PrettyTable, total_days: str) -> dict:
    """
    Convert the PrettyTable to a dictionary for file output
    """
    table = {
        "total_libyears_behind": total_days,
        "libraries": [],
    }
    pt.field_names = ["library", "current_version", "latest_version", "libyears_behind"]
    json_data = pt.get_json_string()
    data = json.loads(json_data)
    # the first element is the field names which we don't want
    table["libraries"] = data[1:]

    return table


def _write_to_json_file(data, file_name: str = "results.json"):
    """
    Write the results to a JSON file
    """
    with open(file_name, "w") as f:
        f.write(data)

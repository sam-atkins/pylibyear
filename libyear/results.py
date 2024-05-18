import json
from dataclasses import dataclass

from prettytable import PrettyTable

from libyear.pypi import get_lib_days
from libyear.utils import get_requirement_name_and_version


@dataclass
class Results:
    table: PrettyTable
    total_days: float


def calculate_results(
    requirements: set,
    sort: bool = False,
):
    """
    Calculate the libyears behind for each library in the requirements
    """
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

    total_days = round(total_days / 365, 2)

    result = Results(pt, total_days)
    return result


def results_to_stdout(data: Results):
    """
    Print the results to the console
    """
    if data.total_days == 0.0:
        print("Your system is up-to-date!")
    else:
        print(data.table)
        print(f"Your system is {str(data.total_days)} libyears behind")


def results_to_json(data: Results, file_name: str):
    """
    Prepare the results in JSON format and write to a file
    """
    table = _prepare_data_for_file_output(
        pretty_table=data.table, total_days=data.total_days
    )
    result = json.dumps(table, indent=4)
    _write_to_json_file(data=result, file_name=file_name)


def _prepare_data_for_file_output(pretty_table: PrettyTable, total_days: float) -> dict:
    """
    Convert the PrettyTable to a dictionary for file output
    """
    table = {
        "total_libyears_behind": str(total_days),
        "libraries": [],
    }
    pretty_table.field_names = [
        "library",
        "current_version",
        "latest_version",
        "libyears_behind",
    ]
    json_data = pretty_table.get_json_string()
    data = json.loads(json_data)
    # NOTE the first element is the field names which we don't want
    table["libraries"] = data[1:]

    return table


def _write_to_json_file(data, file_name: str = "results.json"):
    """
    Write the results to a JSON file
    """
    print(f"Writing results to {file_name}")
    with open(file_name, "w") as f:
        f.write(data)

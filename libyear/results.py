from prettytable import PrettyTable

from libyear.pypi import get_lib_days
from libyear.utils import get_requirement_name_and_version


def print_results_table(requirements: set, sort: bool = False):
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

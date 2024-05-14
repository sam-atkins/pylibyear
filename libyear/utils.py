import re

REQUIREMENT_NAME_RE = r"^([^=><]+)"
REQUIREMENT_VERSION_LT_RE = r"<([^$,]*)"
REQUIREMENT_VERSION_LTE_RE = r"[<=]=([^$,]*)"


def get_requirement_name_and_version(requirement):
    no_requirement = None, None, None
    # Remove comments if they are on the same line
    requirement = requirement.split()[0].strip()
    if not requirement:
        return no_requirement

    name = re.findall(REQUIREMENT_NAME_RE, requirement)
    if not name:
        return no_requirement

    version = re.findall(REQUIREMENT_VERSION_LTE_RE, requirement)
    version_lt = re.findall(REQUIREMENT_VERSION_LT_RE, requirement)
    if not version_lt and not version:
        return no_requirement

    if version:
        return name[0], version[0], None
    return name[0], None, version_lt[0]


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, or editable.
    """
    # Remove whitespace at the start/end of the line
    line = line.strip()

    # Skip blank lines, comments, and editable installs
    return not (
        line == ""
        or line.startswith("-r")
        or line.startswith("#")
        or line.startswith("-e")
        or line.startswith("git+")
        or line.startswith("--")
    )


def load_requirements(requirement_path):
    """
    Load all requirements from the specified requirements file.
    Returns a list of requirement strings.
    """
    requirements = set()
    requirements.update(
        line.strip()
        for line in open(requirement_path).readlines()
        if is_requirement(line)
    )
    return list(requirements)

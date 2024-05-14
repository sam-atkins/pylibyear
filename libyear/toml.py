"""
Module for parsing pyproject.toml files
"""

import tomllib


def load_requirements_from_toml(file_path) -> list[str]:
    """
    Get the libraries from a pyproject.toml file
    """
    with open(file_path, "rb") as f:
        data = tomllib.load(f)

    libraries = []

    # poetry
    prod_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    if prod_deps:
        for key, value in prod_deps.items():
            if key == "python":
                continue
            version = _strip_poetry_version_constraints(value)
            new_lib = f"{key}=={version} \\"
            libraries.append(new_lib)

    dev_deps = data.get("tool", {}).get("poetry", {}).get("dev-dependencies", {})
    if dev_deps:
        for key, value in dev_deps.items():
            version = _strip_poetry_version_constraints(value)
            new_lib = f"{key}=={version} \\"
            libraries.append(new_lib)

    group_dev_deps = (
        data.get("tool", {})
        .get("poetry", {})
        .get("group", {})
        .get("dev", {})
        .get("dependencies", {})
    )
    if group_dev_deps:
        for key, value in group_dev_deps.items():
            version = _strip_poetry_version_constraints(value)
            new_lib = f"{key}=={version} \\"
            libraries.append(new_lib)

    # standard
    std_prod_deps = data.get("project", {}).get("dependencies", {})
    if std_prod_deps:
        for dep in std_prod_deps:
            new_lib = f"{dep} \\"
            libraries.append(new_lib)

    std_opt_deps = data.get("project", {}).get("optional-dependencies", {})
    if std_opt_deps:
        # for k,v in std_opt_deps.values(): print(k, v))
        for items in std_opt_deps.values():
            for dep in items:
                new_lib = f"{_replace_pyproject_constraints(dep)} \\"
                libraries.append(new_lib)

    return libraries


def _strip_poetry_version_constraints(version: str):
    """
    Strip the version constraints from a poetry version string
    """
    return "".join([c for c in version if c.isdigit() or c == "."])


def _replace_pyproject_constraints(version: str):
    """
    Replace the version constraints from a poetry version string.
    This is a hack to make the version constraints compatible
    with the script, but it needs updating.
    """
    return (
        version.replace(">=", "==")
        .replace(">", "==")
        .replace("<", "==")
        .replace("<=", "==")
    )

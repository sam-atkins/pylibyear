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

    return libraries


def _strip_poetry_version_constraints(version: str):
    """
    Strip the version constraints from a poetry version string
    """
    return "".join([c for c in version if c.isdigit() or c == "."])

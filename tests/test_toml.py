from pathlib import Path

import pytest

from libyear.toml import _strip_poetry_version_constraints, get_libraries_from_toml_file


def test_get_libraries_from_toml_file():
    pyproject_toml_path = str(Path(__file__).parent / "data" / "pyproject_poetry.toml")
    result = get_libraries_from_toml_file(pyproject_toml_path)
    assert result == [
        {
            "name": "flask",
            "version": "3.0.0",
        },
        {
            "name": "flask-restx",
            "version": "1.0.5",
        },
        {
            "name": "autoflake",
            "version": "1.3.0",
        },
        {
            "name": "black",
            "version": "24.0.0",
        },
        {
            "name": "coverage",
            "version": "7.4.0",
        },
        {
            "name": "ruff",
            "version": "0.3.5",
        },
        {
            "name": "pytest",
            "version": "8.1.1",
        },
    ]


@pytest.mark.parametrize(
    "input, expected",
    [
        ("^1.0.0", "1.0.0"),
        ("~1.0.0", "1.0.0"),
        ("1.2.*", "1.2."),
    ],
)
def test_strip_poetry_version_constraints(input, expected):
    result = _strip_poetry_version_constraints(input)
    assert result == expected

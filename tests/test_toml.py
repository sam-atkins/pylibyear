from pathlib import Path

import pytest

from libyear.toml import _strip_poetry_version_constraints, load_requirements_from_toml


def test_get_libraries_from_toml_file():
    pyproject_toml_path = str(Path(__file__).parent / "data" / "pyproject_poetry.toml")
    result = load_requirements_from_toml(pyproject_toml_path)
    assert result == [
        "flask==3.0.0 \\",
        "flask-restx==1.0.5 \\",
        "autoflake==1.3 \\",
        "black==24.0.0 \\",
        "coverage==7.4.0 \\",
        "ruff==0.3.5 \\",
        "pytest==8.1.1 \\",
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

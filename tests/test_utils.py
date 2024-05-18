from pathlib import Path

import pytest
import typer

from libyear.utils import (
    get_requirement_name_and_version,
    load_requirements,
    validate_file_path,
)


def test_loads_from_requirements_file_with_hashes():
    path = Path(__file__).parent / "data" / "requirements.txt"
    assert any(line.startswith("appdirs") for line in load_requirements(path))


def test_gets_name_and_version_from_requirements_file_with_hashes():
    path = Path(__file__).parent / "data" / "requirements.txt"
    results = {
        get_requirement_name_and_version(line) for line in load_requirements(path)
    }

    assert ("appdirs", "1.4.3", None) in results


@pytest.mark.parametrize(
    "invalid_file_arg",
    [
        ("invalid_path"),
        ("libyear"),
    ],
)
def test_validate_file_path_raises(invalid_file_arg):
    with pytest.raises(typer.BadParameter):
        validate_file_path(invalid_file_arg)


def test_validate_file_path_():
    path = Path(__file__).parent / "data" / "requirements.txt"
    result = validate_file_path(path)
    assert result == path

import json
import os
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from libyear.main import app


@pytest.fixture(scope="module")
def vcr_config():
    return {"decode_compressed_response": True}


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    # Put all cassettes in tests/cassettes/{module}/{test}.yaml
    return os.path.join("tests/cassettes/", request.module.__name__)


@pytest.mark.vcr()
def test_libyear_main_output():
    requirements_path = str(Path(__file__).parent / "data" / "requirements.txt")
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "text",
            requirements_path,
            "--sort",
        ],
    )

    out = result.stdout
    out_lst = out.split("\n")

    assert result.exit_code == 0

    assert (
        out_lst[0:3]
        == """\
+-------------------+-----------------+----------------+-----------------+
|      Library      | Current Version | Latest Version | Libyears behind |
+-------------------+-----------------+----------------+-----------------+""".split(
            "\n"
        )
    )

    ref_lst = """\
|        argh       |      0.26.2     |     0.31.3     |       8.18      |
|       rerun       |      1.0.30     |     1.0.31     |       7.41      |
|       click       |       7.0       |     8.3.1      |       7.14      |
|      nodeenv      |      1.3.3      |     1.10.0     |       7.13      |
|      coverage     |      4.5.3      |     7.13.4     |       6.92      |
|       isort       |      4.3.17     |     8.0.0      |       6.87      |
|      filelock     |      3.0.12     |     3.24.3     |       6.76      |
|   pytest-testmon  |      0.9.16     |     2.2.0      |       6.72      |
|       pytest      |      4.4.0      |     9.0.2      |       6.69      |
|   flake8-bugbear  |      19.3.0     |    25.11.29    |       6.68      |
|  mypy-extensions  |      0.4.1      |     1.1.0      |       6.67      |
|     virtualenv    |      16.6.2     |    20.38.0     |       6.61      |
|       attrs       |      19.1.0     |     25.4.0     |       6.6       |
|      identify     |      1.4.5      |     2.6.16     |       6.58      |
|   more-itertools  |      7.0.0      |     10.8.0     |       6.44      |
|    pycodestyle    |      2.5.0      |     2.14.0     |       6.39      |
|     packaging     |       19.2      |      26.0      |       6.35      |
|        cfgv       |      2.0.1      |     3.5.0      |       6.34      |
|      pathspec     |      0.6.0      |     1.0.4      |       6.32      |
|       flake8      |      3.7.7      |     7.3.0      |       6.32      |
|       pyyaml      |      5.1.1      |     6.0.3      |       6.31      |
|      pyflakes     |      2.1.1      |     3.4.0      |       6.31      |
|       black       |     19.10b0     |     26.1.0     |       6.23      |
|        tox        |      3.14.2     |     4.44.0     |       6.22      |
|       regex       |    2019.12.9    |   2026.2.19    |       6.2       |
|     pyparsing     |      2.4.5      |     3.3.2      |       6.2       |
|      watchdog     |      0.9.0      |     6.0.0      |       6.18      |
|     pre-commit    |      1.20.0     |     4.5.1      |       6.14      |
|        mypy       |      0.750      |     1.19.1     |       6.05      |
|        six        |      1.12.0     |     1.17.0     |       5.99      |
| typing-extensions |     3.7.4.1     |     4.15.0     |       5.83      |
|       pluggy      |      0.13.1     |     1.6.0      |       5.48      |
|       mccabe      |      0.6.1      |     0.7.0      |       4.99      |
|     typed-ast     |      1.4.0      |     1.5.5      |       4.08      |
|      colorama     |      0.4.1      |     0.4.6      |       3.92      |
|      appdirs      |      1.4.3      |     1.4.4      |       3.18      |
|    entrypoints    |       0.3       |      0.4       |       3.07      |
|         py        |      1.8.0      |     1.11.0     |       2.7       |
|        toml       |      0.10.0     |     0.10.2     |       2.08      |
|      psycopg      |      3.2.9      |     3.3.3      |       0.77      |\
""".split("\n")

    def table_sort(s):
        """remove `|` + any spaces, in order to get alphabetic sort of first column"""
        return s.lstrip(" |")

    assert sorted(out_lst[3:-3], key=table_sort) == sorted(ref_lst, key=table_sort)

    assert (
        out_lst[-3:]
        == """\
+-------------------+-----------------+----------------+-----------------+
Your system is 233.04 libyears behind
""".split("\n")
    )


@pytest.mark.vcr()
def test_libyear_main_output_to_json():
    tmp_file = tempfile.NamedTemporaryFile()
    requirements_path = str(Path(__file__).parent / "data" / "requirements.txt")
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "text",
            requirements_path,
            "--json",
            tmp_file.name,
        ],
    )

    assert result.exit_code == 0
    with open(tmp_file.name, "r") as f:
        json_data = f.read()
        data = json.loads(json_data)
        assert data["total_libyears_behind"] == "233.04"
        assert len(data["libraries"]) == 40


@pytest.mark.vcr()
def test_json_output_creates_file_and_parent_directories():
    """
    GIVEN a requirements.txt file and a --json output path where neither
          the file nor its parent directories exist
    WHEN the text command is invoked with --json pointing to that path
    THEN the parent directories and JSON file are created with valid output
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_path = os.path.join(tmp_dir, "nested", "dir", "results.json")
        requirements_path = str(Path(__file__).parent / "data" / "requirements.txt")
        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "text",
                requirements_path,
                "--json",
                output_path,
            ],
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)
        with open(output_path, "r") as f:
            data = json.loads(f.read())
            assert "total_libyears_behind" in data
            assert "libraries" in data

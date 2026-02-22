# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`pylibyear` is a CLI tool that measures Python dependency freshness in "libyears" — a single number representing how far behind your dependencies are from their latest versions. It queries the PyPI API to compare current vs latest release dates.

The CLI entry point is `libyear` (defined in `pyproject.toml` → `[project.scripts]`), with two subcommands: `text` (for requirements.txt) and `toml` (for pyproject.toml).

## Setup

```bash
uv pip install -r pyproject.toml --all-extras
uv pip install -e .
```

## Commands

Uses [just](https://github.com/casey/just) as a command runner (`justfile`):

```bash
just lint      # ruff check --fix && ruff format
just test      # pytest
just testv     # pytest -vv
just check     # lint + test
just build     # build package for distribution
just bump      # bump version in libyear/__about__.py
```

Run a single test:
```bash
pytest tests/test_libyear.py::test_libyear_main_output
```

## Architecture

```
libyear/
  main.py      # Typer CLI app; defines `text` and `toml` subcommands
  pypi.py      # PyPI API calls; computes lib days between current and latest release
  toml.py      # Parses pyproject.toml (supports standard PEP 621 + Poetry formats)
  utils.py     # Parses requirements.txt lines; regex-based version extraction
  results.py   # Aggregates results into a PrettyTable; outputs to stdout or JSON
  __about__.py # Version string
```

**Data flow:** CLI command → load requirements (utils/toml) → for each dep, call PyPI API (pypi.py) → compute days difference → aggregate into `Results` dataclass (results.py) → render to stdout or write JSON file.

## Tests

Tests use `pytest-vcr` to record/replay HTTP interactions with PyPI. Cassettes are stored in `tests/cassettes/{module}/{test}.yaml`. The `@pytest.mark.vcr()` decorator enables cassette replay for a test.

When adding new tests that call PyPI, run once with network access to record the cassette, then subsequent runs use the recorded response.

## Version Management

Version is defined in `libyear/__about__.py`. Use `just bump` (runs `scripts/version_bump.py`) to increment it.

# List available recipes
default:
    just --list

# Install the dependencies using uv
[group('dev')]
install:
    uv sync
    uv pip install -e .

# Run libyear against a requirements file
[group('dev')]
run path:
    uv run libyear text {{path}}

# Lint and run tests
[group('code quality')]
check: lint test

# Lint, format and type check the code
[group('code quality')]
lint:
    uv run ruff check --fix
    uv run ruff format
    uv run ty check

# Runs the tests
[group('code quality')]
test:
    uv run pytest

# Runs the tests with verbose output
[group('code quality')]
testv:
    uv run pytest -vv

# Build the package for distribution
[group('build')]
build:
    rm -rf dist/**
    uv build

# Bump the version in libyear/__about__.py
[group('build')]
bump:
    python scripts/version_bump.py

# Release a new version: update version, commit, tag, push, and create GitHub release
[group('build')]
release version:
    python scripts/version_bump.py {{version}}
    git add pyproject.toml libyear/__about__.py
    git commit -m "release v{{version}}"
    git tag -a v{{version}} -m "v{{version}}"
    git push origin HEAD --tags
    gh release create v{{version}} --generate-notes

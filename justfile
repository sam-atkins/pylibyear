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

# Release a new version: tag, push, and create GitHub release
[group('build')]
release version:
    git tag -a v{{version}} -m "v{{version}}"
    git push origin v{{version}}
    gh release create v{{version}} --generate-notes --repo sam-atkins/pylibyear

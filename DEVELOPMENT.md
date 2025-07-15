# Setup

Install ![uv](https://docs.astral.sh/uv/getting-started/installation/) and then run `uv sync --dev`.

# Running tests

The tests will initialize airflow under ./.airflow.

Run `AIRFLOW_HOME=$PWD/.airflow uv run pytest` to run all the tests.

# Building a package

Run `uv build`.

# Publishing a package

Get an api token from PyPI and run `uv config pypi-token.pypi my-token`.

To publish the package you just built, run `uv publish`.

Don't forget to create a git tag for the version you just released!

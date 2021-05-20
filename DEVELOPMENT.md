# Setup

1. Install ![pyenv](https://github.com/pyenv/pyenv) and then run `pyenv install`.
2. Install ![poetry](https://python-poetry.org/) and then run `poetry install`.

# Running tests

The tests will initialize airflow under ~/airflow.

Run `poetry run pytest` to run all the tests.

# Building a package

Run `poetry build`.

# Publishing a package

Get an api token from PyPI and run `poetry config pypi-token.pypi my-token`.

To publish the package you just built, run `poetry publish`.

Don't forget to create a git tag for the version you just released!

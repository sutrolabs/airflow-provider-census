# Changelog

## 2.1.0 — 2026-04-02

- Raised the supported Python floor to 3.10+
- Added `apache-airflow-providers-common-compat` and updated provider imports for Airflow 2.10+/3.x compatibility
- Added a deferrable `CensusSensor` powered by a new `CensusTrigger`
- Added `CensusHook.test_connection()` support for Airflow UI/CLI connection testing
- Updated user-facing text to reflect that Census is now Fivetran Activations
- Added a task extra link back to the Fivetran Activations sync history view
- Refreshed the example DAG and README for the current Activations API docs and compatibility story
- A future `3.0.0` release is planned to remove the Census names from code and drop Airflow 2.x support

## 2.0.0 — 2025-07-15

- Modernized provider packaging (migrated from Poetry/setup.cfg to pyproject.toml)
- Added support for Python 3.9, 3.10, 3.11, 3.12, 3.13

## 1.4.0 — 2025-07-14

- Added initial Airflow 3 support with conditional import shims

## 1.2.0 — 2024-09-12

- Weakened `apache-airflow-providers-http` dependency constraint for broader compatibility

## 1.1.1 — 2021-06-18

- Incorporated Astronomer suggestions for provider best practices
## 1.1.0 — 2021-06-07

- Added `CensusSensor` with polling support to monitor sync run status

## 1.0.0 — 2021-05-20

- Initial release with Airflow 2.0 support
- `CensusHook` — HTTP hook with Bearer token auth against the Census API
- `CensusOperator` — triggers a Census sync run
- Connection UI integration with custom field labels and hidden fields
- Python 3.5+ support

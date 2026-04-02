# Fivetran Activations Provider for Apache Airflow

This package lets you trigger and monitor Fivetran Activations syncs from Apache Airflow.

## Support Matrix

- Python: `>=3.10`
- Apache Airflow: `>=2.10,<4`
- Airflow authoring compatibility: Airflow `2.10+` and `3.x`

## Installation

Install the package from PyPI with your preferred Python package manager.

```bash
pip install airflow-provider-census
```

## Connection Setup

The provider uses the `census_default` connection ID by default.

Create a connection in the Airflow UI with:

- Conn Id: `census_default`
- Conn Type: `Census` (kept for backward compatibility)
- Host: `app.getcensus.com` for US workspaces or `app-eu.getcensus.com` for EU workspaces
- Activations API Token: your Fivetran Activations API token

The hook implements `test_connection()`, so Airflow's Test Connection button and `airflow connections test` CLI command can validate the setup.

## Hooks

```python
from airflow_provider_census.hooks.census import CensusHook
```

`CensusHook` extends `HttpHook` and provides helpers to:

- trigger a sync run
- fetch sync run status
- test the Airflow connection configuration

## Operator

```python
from airflow_provider_census.operators.census import CensusOperator
```

`CensusOperator` triggers a Fivetran Activations sync run and returns the resulting `sync_run_id` via XCom.

Parameters:

- `sync_id`: the Fivetran Activations sync ID, for example from `https://app.getcensus.com/syncs/<SYNC_ID>/overview`
- `census_conn_id`: optional connection ID, defaults to `census_default`

The operator also exposes a `Fivetran Activations Sync Run` task link in the Airflow UI.

## Sensor

```python
from airflow_provider_census.sensors.census import CensusSensor
```

`CensusSensor` waits for a Fivetran Activations sync run to complete.

Parameters:

- `sync_run_id`: the sync run ID returned by `CensusOperator`
- `census_conn_id`: optional connection ID, defaults to `census_default`
- `deferrable`: when `True`, defers polling to the triggerer instead of holding a worker slot

When `deferrable=True`, your Airflow deployment must be running a triggerer.

## Example DAG

```python
from datetime import datetime
from datetime import timedelta

from airflow.providers.common.compat.sdk import DAG

from airflow_provider_census.operators.census import CensusOperator
from airflow_provider_census.sensors.census import CensusSensor

with DAG(
    dag_id="example_census",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:
    trigger_sync = CensusOperator(
        task_id="trigger_sync",
        census_conn_id="census_default",
        sync_id=27,
    )

    wait_for_sync = CensusSensor(
        task_id="wait_for_sync",
        sync_run_id="{{ ti.xcom_pull(task_ids='trigger_sync') }}",
        census_conn_id="census_default",
        deferrable=True,
    )

    trigger_sync >> wait_for_sync
```

## API Documentation

The Activations Management API reference now lives in Fivetran documentation:

- https://fivetran.com/docs/activations/rest-api/api-reference/introduction

## Feedback

Source code: https://github.com/sutrolabs/airflow-provider-census

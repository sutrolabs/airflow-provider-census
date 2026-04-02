from datetime import datetime
from datetime import timedelta

from airflow.providers.common.compat.sdk import DAG

from airflow_provider_census.operators.census import CensusOperator
from airflow_provider_census.sensors.census import CensusSensor

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="example_census",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
) as dag:
    sync = CensusOperator(
        task_id="sync",
        census_conn_id="census_default",
        sync_id=4895,
    )

    sensor = CensusSensor(
        task_id="sensor",
        sync_run_id="{{ ti.xcom_pull(task_ids='sync') }}",
        census_conn_id="census_default",
        deferrable=True,
    )

    sync >> sensor

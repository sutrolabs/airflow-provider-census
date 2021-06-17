from airflow_provider_census.operators.census import CensusOperator
from airflow_provider_census.sensors.census import CensusSensor

from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('census', max_active_runs = 1, default_args = default_args)

sync = CensusOperator(sync_id = 27, dag = dag, task_id = 'sync')

sensor = CensusSensor(sync_run_id = "{{ ti.xcom_pull(task_ids = 'sync') }}", dag = dag, task_id = 'sensor')

sync >> sensor

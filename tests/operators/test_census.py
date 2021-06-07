from airflow_provider_census.operators.census import CensusOperator

from airflow.exceptions import AirflowException, AirflowTaskTimeout
import pytest

class TestCensusOperator:
    def test_census_operator(self, requests_mock):
        trigger_json = {
            'status': 'success',
            'data': {
                'sync_run_id': 0
            }
        }
        requests_mock.post('https://app.getcensus.com/api/v1/syncs/0/trigger', json = trigger_json)
        operator = CensusOperator(sync_id = 0, wait = False, task_id = 'census_operator')
        operator.execute(None)

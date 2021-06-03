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
        operator.execute({})

    def test_census_operator_waiting(self, requests_mock):
        trigger_json = {
            'status': 'success',
            'data': {
                'sync_run_id': 0
            }
        }
        requests_mock.post('https://app.getcensus.com/api/v1/syncs/0/trigger', json = trigger_json)

        run_sync_responses = [
            {
                'status_code': 200,
                'json': {
                    'status': 'success',
                    'data': {
                        'status': 'working'
                    }
                }
            },
            {
                'status_code': 200,
                'json': {
                    'status': 'success',
                    'data': {
                        'status': 'completed'
                    }
                }
            }
        ]
        requests_mock.register_uri('GET', 'https://app.getcensus.com/api/v1/sync_runs/0', run_sync_responses)

        operator = CensusOperator(sync_id = 0, wait_seconds = 1, task_id = 'census_operator')
        operator.execute({})

    def test_census_operator_failed_status(self, requests_mock):
        trigger_json = {
            'status': 'success',
            'data': {
                'sync_run_id': 0
            }
        }
        requests_mock.post('https://app.getcensus.com/api/v1/syncs/0/trigger', json = trigger_json)

        run_sync_responses = [
            {
                'status_code': 200,
                'json': {
                    'status': 'success',
                    'data': {
                        'status': 'working'
                    }
                }
            },
            {
                'status_code': 200,
                'json': {
                    'status': 'success',
                    'data': {
                        'error_message': 'borked',
                        'status': 'failed'
                    }
                }
            }
        ]
        requests_mock.register_uri('GET', 'https://app.getcensus.com/api/v1/sync_runs/0', run_sync_responses)

        operator = CensusOperator(sync_id = 0, wait_seconds = 1, task_id = 'census_operator')

        with pytest.raises(AirflowException) as excinfo:
            operator.execute({})

            assert 'Sync 0 failed for sync run 0 with error "borked"' == excinfo.value

    def test_census_operator_timed_out(self, requests_mock):
        trigger_json = {
            'status': 'success',
            'data': {
                'sync_run_id': 0
            }
        }
        requests_mock.post('https://app.getcensus.com/api/v1/syncs/0/trigger', json = trigger_json)

        run_sync_responses = [
            {
                'status_code': 200,
                'json': {
                    'status': 'success',
                    'data': {
                        'status': 'working'
                    }
                }
            }
        ]
        requests_mock.register_uri('GET', 'https://app.getcensus.com/api/v1/sync_runs/0', run_sync_responses)

        operator = CensusOperator(sync_id = 0, wait_seconds = 1, timeout_seconds = 1, task_id = 'census_operator')

        with pytest.raises(AirflowTaskTimeout) as excinfo:
            operator.execute({})

            assert 'Timed out for sync 0 while waiting for sync run 0' == excinfo.value

from airflow_provider_census.operators.census import CensusOperator

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

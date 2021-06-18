from airflow_provider_census.sensors.census import CensusSensor

from airflow.exceptions import AirflowException
import pytest

class TestCensusSensor:
    """
    Test functions for Census Sensor.
    """

    def test_poke_working(self, requests_mock):
        sync_run_info_json = {
            'status': 'success',
            'data': {
                'status': 'working'
            }
        }
        requests_mock.get('https://app.getcensus.com/api/v1/sync_runs/0', json = sync_run_info_json)

        sensor = CensusSensor(sync_run_id = 0, task_id = 'census_sensor')

        assert not sensor.poke(None)

    def test_poke_failed(self, requests_mock):
        sync_run_info_json = {
            'status': 'success',
            'data': {
                'error_message': 'something broke',
                'status': 'failed'
            }
        }
        requests_mock.get('https://app.getcensus.com/api/v1/sync_runs/0', json = sync_run_info_json)

        sensor = CensusSensor(sync_run_id = 0, task_id = 'census_sensor')

        with pytest.raises(AirflowException) as excinfo:
            sensor.poke(None)

            assert 'Census sync run 0 failed with error: something broke' == excinfo.value

    def test_poke_completed(self, requests_mock):
        sync_run_info_json = {
            'status': 'success',
            'data': {
                'status': 'completed'
            }
        }
        requests_mock.get('https://app.getcensus.com/api/v1/sync_runs/0', json = sync_run_info_json)

        sensor = CensusSensor(sync_run_id = 0, task_id = 'census_sensor')

        assert sensor.poke(None)

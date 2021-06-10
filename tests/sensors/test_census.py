import pytest
import requests_mock
import unittest
from unittest import mock

from airflow_provider_census.sensors.census import CensusSensor
from airflow.exceptions import AirflowException


# Mock the `census_default` Airflow connection 
@mock.patch.dict('os.environ', AIRFLOW_CONN_CENSUS_DEFAULT='http://API_KEY:API_SECRET@')
class TestCensusSensor(unittest.TestCase):
    """ 
    Test functions for Census Sensor. 
    """

    @requests_mock.mock()
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

    @requests_mock.mock()
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

    @requests_mock.mock()
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

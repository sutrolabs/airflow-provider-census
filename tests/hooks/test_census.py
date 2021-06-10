import pytest
import requests_mock
import unittest
from unittest import mock

from airflow_provider_census.hooks.census import CensusHook


# Mock the `census_default` Airflow connection 
@mock.patch.dict('os.environ', AIRFLOW_CONN_CENSUS_DEFAULT='http://API_KEY:API_SECRET@')
class TestCensusHook(unittest.TestCase):
    """ 
    Test functions for Census Hook. 

    Mocks responses from Census API.
    """

    @requests_mock.mock()
    def test_get_conn(self, requests_mock):
        hook = CensusHook()
        session = hook.get_conn(None)
        assert 'Authorization' in session.headers
        assert session.headers['Authorization'] == 'Bearer API_SECRET'

    @requests_mock.mock()
    def test_trigger_sync(self, requests_mock):
        trigger_json = {
            'status': 'success',
            'data': {
                'sync_run_id': 1
            }
        }
        requests_mock.post('https://app.getcensus.com/api/v1/syncs/0/trigger', json = trigger_json)

        hook = CensusHook()
        sync_run_id = hook.trigger_sync(0)

        assert 1 == sync_run_id

    @requests_mock.mock()
    def test_get_sync_run_info(self, requests_mock):
        sync_run_info_json = {
            'status': 'success',
            'data': {
                'status': 'working'
            }
        }
        requests_mock.get('https://app.getcensus.com/api/v1/sync_runs/0', json = sync_run_info_json)

        hook = CensusHook()
        info = hook.get_sync_run_info(0)

        assert info['status'] == 'working'

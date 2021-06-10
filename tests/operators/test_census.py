import pytest
import requests_mock
import unittest
from unittest import mock

from airflow_provider_census.operators.census import CensusOperator
from airflow.exceptions import AirflowException, AirflowTaskTimeout



# Mock the `census_default` Airflow connection 
@mock.patch.dict('os.environ', AIRFLOW_CONN_CENSUS_DEFAULT='http://API_KEY:API_SECRET@')
class TestCensusOperator(unittest.TestCase):
    """ 
    Test functions for Census Operator. 

    Mocks responses from Census API.
    """

    @requests_mock.mock()
    def test_census_operator(self, requests_mock):
        trigger_json = {
            'status': 'success',
            'data': {
                'sync_run_id': 0
            }
        }
        requests_mock.post('https://app.getcensus.com/api/v1/syncs/0/trigger', json = trigger_json)
        operator = CensusOperator(sync_id = 0, task_id = 'census_operator')
        operator.execute(None)

import vcr

from airflow_provider_census.operators.census import CensusOperator

class TestCensusOperator:
    @vcr.use_cassette()
    def test_census_operator(self):
        operator = CensusOperator(sync_id = 0, task_id = 'census_operator')
        operator.execute({})

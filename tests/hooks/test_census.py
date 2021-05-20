from airflow_provider_census.hooks.census import CensusHook

class TestCensusHook:
    def test_get_conn(self):
        hook = CensusHook()
        session = hook.get_conn(None)
        assert 'Authorization' in session.headers
        assert session.headers['Authorization'] == 'Bearer secret-token:census'

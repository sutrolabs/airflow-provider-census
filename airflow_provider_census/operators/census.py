from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from typing import Any

from airflow_provider_census.hooks.census import CensusHook

class CensusOperator(BaseOperator):
    '''
    `CensusOperator` interacts with the Census API
    '''

    @apply_defaults
    def __init__(self, sync_id: int, census_conn_id: str = 'census_default', **kwargs):
        super().__init__(**kwargs)
        self.sync_id = sync_id
        self.census_conn_id = census_conn_id

    def _get_hook(self) -> CensusHook:
        return CensusHook(census_conn_id = self.census_conn_id)

    def execute(self, context) -> Any:
        endpoint = 'api/v1/syncs/{sync_id}/trigger'.format(sync_id = self.sync_id)
        hook = self._get_hook()
        response = hook.run(endpoint)
        response.raise_for_status()

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import time
from typing import Any

from airflow_provider_census.hooks.census import CensusHook

class CensusOperator(BaseOperator):
    '''
    `CensusOperator` interacts with the Census API
    '''

    @apply_defaults
    def __init__(self, sync_id: int, wait: bool = True, wait_seconds: int = 60, timeout_seconds: float = float('inf'), census_conn_id: str = 'census_default', **kwargs):
        super().__init__(**kwargs)
        self.sync_id = sync_id
        self.wait = wait
        self.wait_seconds = wait_seconds
        self.timeout_seconds = timeout_seconds
        self.census_conn_id = census_conn_id

    def _get_hook(self) -> CensusHook:
        return CensusHook(census_conn_id = self.census_conn_id)

    def execute(self, context) -> Any:
        endpoint = 'api/v1/syncs/{sync_id}/trigger'.format(sync_id = self.sync_id)
        hook = self._get_hook()
        response = hook.run(endpoint)
        response.raise_for_status()

        if self.wait:
            body = response.json()
            sync_run_id = body['data']['sync_run_id']
            poll_endpoint = 'api/v1/sync_runs/{sync_run_id}'.format(sync_run_id = sync_run_id)
            poll_hook = CensusHook(census_conn_id = self.census_conn_id, method = 'GET')
            terminal_status_set = {'completed', 'failed'}

            start = time.monotonic()
            while time.monotonic() - start < self.timeout_seconds:
                poll_response = poll_hook.run(poll_endpoint)
                poll_response.raise_for_status()

                poll_body = poll_response.json()
                status = poll_body['data']['status']

                if status in terminal_status_set:
                    break

                time.sleep(self.wait_seconds)

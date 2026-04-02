from airflow.providers.common.compat.sdk import BaseOperator

from typing import Any

from airflow_provider_census.hooks.census import CensusHook
from airflow_provider_census.links.census import CensusSyncRunLink


class CensusOperator(BaseOperator):
    """Triggers a sync with the Fivetran Activations API.

    :param sync_id: Fivetran Activations sync ID
    :type sync_id: int
    :param census_conn_id: `Conn ID` of the Connection to be used to configure this hook.
    :type census_conn_id: str
    """

    operator_extra_links = (CensusSyncRunLink(),)

    def __init__(self, sync_id: int, census_conn_id: str = "census_default", **kwargs) -> None:
        super().__init__(**kwargs)
        self.sync_id = sync_id
        self.census_conn_id = census_conn_id

    def _get_hook(self) -> CensusHook:
        return CensusHook(census_conn_id=self.census_conn_id)

    def execute(self, context) -> Any:
        hook = self._get_hook()

        return hook.trigger_sync(self.sync_id)

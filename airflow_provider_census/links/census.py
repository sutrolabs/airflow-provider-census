from __future__ import annotations

from airflow.models.xcom import XCom
from airflow.providers.common.compat.sdk import BaseOperatorLink

from airflow_provider_census.hooks.census import CensusHook


class CensusSyncRunLink(BaseOperatorLink):
    name = "Fivetran Activations Sync Run"

    def get_link(self, operator, dttm=None, ti_key=None) -> str | None:
        sync_run_id = None
        if ti_key is not None:
            sync_run_id = XCom.get_value(key="return_value", ti_key=ti_key)
        elif dttm is not None:
            sync_run_id = XCom.get_one(
                key="return_value",
                dag_id=operator.dag_id,
                task_id=operator.task_id,
                execution_date=dttm,
            )

        if not sync_run_id:
            return None

        hook = CensusHook(census_conn_id=getattr(operator, "census_conn_id", CensusHook.default_conn_name))
        sync_id = getattr(operator, "sync_id", None)
        if sync_id is None:
            return f"{hook.get_api_base_url()}/sync-runs/{sync_run_id}"

        return hook.get_sync_history_url(sync_id=sync_id, sync_run_id=sync_run_id)

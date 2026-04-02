from __future__ import annotations

from airflow.models.xcom import XCom
from airflow.providers.common.compat.sdk import BaseOperatorLink

from airflow_provider_census.hooks.census import CensusHook


class CensusSyncRunLink(BaseOperatorLink):
    name = "Fivetran Activations Sync Run"

    def get_link(self, operator, dttm=None, ti_key=None) -> str | None:
        # Operator links are rendered by the webserver, not from task execution
        # code, so a direct XCom lookup here does not violate Airflow 3 task
        # isolation constraints.
        sync_run_id = None
        if ti_key is not None:
            sync_run_id = XCom.get_value(key="return_value", ti_key=ti_key)
        elif dttm is not None:
            get_one = getattr(XCom, "get_one", None)
            if get_one is not None:
                try:
                    sync_run_id = get_one(
                        key="return_value",
                        dag_id=operator.dag_id,
                        task_id=operator.task_id,
                        execution_date=dttm,
                    )
                except TypeError:
                    # Airflow 3 no longer uses execution_date-based XCom lookups.
                    sync_run_id = None

        if not sync_run_id:
            return None

        hook = CensusHook(census_conn_id=getattr(operator, "census_conn_id", CensusHook.default_conn_name))
        sync_id = getattr(operator, "sync_id", None)
        if sync_id is None:
            return f"{hook.get_api_base_url()}/sync-runs/{sync_run_id}"

        return hook.get_sync_history_url(sync_id=sync_id, sync_run_id=sync_run_id)

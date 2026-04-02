from __future__ import annotations

from typing import Any

from airflow.exceptions import AirflowException
from airflow.providers.common.compat.sdk import BaseSensorOperator

from airflow_provider_census.hooks.census import CensusHook
from airflow_provider_census.triggers.census import CensusTrigger


class CensusSensor(BaseSensorOperator):
    """Waits for sync to complete.


    :param sync_run_id: Census sync run ID
    :type sync_run_id: str
    :param census_conn_id: `Conn ID` of the Connection to be used to configure this hook.
    :type census_conn_id: str
    """

    template_fields = ("sync_run_id",)

    def __init__(
        self,
        sync_run_id: str,
        census_conn_id: str = "census_default",
        deferrable: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.sync_run_id = sync_run_id
        self.census_conn_id = census_conn_id
        self.deferrable = deferrable
        self.hook: CensusHook | None = None

    def _get_hook(self) -> CensusHook:
        if self.hook is None:
            self.hook = CensusHook(census_conn_id=self.census_conn_id)
        return self.hook

    def execute(self, context: Any) -> Any:
        if not self.deferrable:
            return super().execute(context)

        if self.poke(context):
            self.log.info("Census sync run %s completed before deferral.", self.sync_run_id)
            return None

        self.defer(
            trigger=CensusTrigger(
                sync_run_id=self.sync_run_id,
                census_conn_id=self.census_conn_id,
                poll_interval=max(float(self.poke_interval), 1.0),
            ),
            method_name="execute_complete",
        )

    def execute_complete(self, context: Any, event: dict[str, Any] | None = None) -> None:
        if not event:
            raise AirflowException("Census trigger returned no event payload.")

        status = event.get("status")
        if status == "completed":
            return None

        if status == "failed":
            error_message = event.get("error_message") or "Unknown error."
            raise AirflowException(
                "Census sync run {sync_run_id} failed with error: {error_message}".format(
                    sync_run_id=event.get("sync_run_id", self.sync_run_id),
                    error_message=error_message,
                )
            )

        raise AirflowException(
            "Census sync run {sync_run_id} returned unexpected status: {status}".format(
                sync_run_id=event.get("sync_run_id", self.sync_run_id),
                status=status,
            )
        )

    def poke(self, context: Any) -> bool:
        hook = self._get_hook()
        info = hook.get_sync_run_info(self.sync_run_id)
        status = info["status"]

        if status == "failed":
            raise AirflowException(
                "Census sync run {sync_run_id} failed with error: {error_message}".format(
                    sync_run_id=self.sync_run_id,
                    error_message=info.get("error_message") or info.get("error_detail") or "Unknown error.",
                )
            )

        return status == "completed"

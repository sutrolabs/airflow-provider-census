from __future__ import annotations

import asyncio
from typing import Any

import aiohttp
from airflow.exceptions import AirflowException
from airflow.triggers.base import BaseTrigger
from airflow.triggers.base import TriggerEvent

from airflow_provider_census.hooks.census import CensusHook


class CensusTrigger(BaseTrigger):
    def __init__(
        self,
        sync_run_id: int | str,
        census_conn_id: str = CensusHook.default_conn_name,
        poll_interval: float = 60.0,
    ) -> None:
        super().__init__()
        self.sync_run_id = sync_run_id
        self.census_conn_id = census_conn_id
        self.poll_interval = float(poll_interval)

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "airflow_provider_census.triggers.census.CensusTrigger",
            {
                "sync_run_id": self.sync_run_id,
                "census_conn_id": self.census_conn_id,
                "poll_interval": self.poll_interval,
            },
        )

    async def run(self):
        while True:
            info = await self._get_sync_run_info()
            status = info["status"]
            if status in {"completed", "failed"}:
                yield TriggerEvent(
                    {
                        "sync_run_id": self.sync_run_id,
                        "status": status,
                        "error_message": info.get("error_message") or info.get("error_detail"),
                    }
                )
                return

            await asyncio.sleep(self.poll_interval)

    async def _get_sync_run_info(self) -> dict[str, Any]:
        hook = CensusHook(census_conn_id=self.census_conn_id)
        url = f"{hook.get_api_base_url()}/api/v1/sync_runs/{self.sync_run_id}"
        timeout = aiohttp.ClientTimeout(total=30)

        async with aiohttp.ClientSession(headers=hook.get_auth_headers(), timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                payload = await response.json()

        if payload.get("status") != "success":
            raise AirflowException("Unexpected response from Census Activations API.")

        return payload["data"]

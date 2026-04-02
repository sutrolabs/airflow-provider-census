from __future__ import annotations

from typing import Any
from typing import Dict

import requests

from airflow.exceptions import AirflowException
from airflow.providers.http.hooks.http import HttpHook


class CensusHook(HttpHook):
    """Census API hook

    :param census_conn_id: `Conn ID` of the Connection to be used to configure this hook.
    :type census_conn_id: str
    """

    conn_name_attr = 'census_conn_id'
    default_conn_name = 'census_default'
    conn_type = 'census'
    hook_name = 'Census'

    @staticmethod
    def get_ui_field_behaviour() -> Dict[str, Any]:
        return {
            "hidden_fields": ["login", "port", "schema", "extra"],
            "relabeling": {
                "host": "Activations API Host",
                "password": "Activations API Token",
            },
            "placeholders": {
                "host": "app.getcensus.com or app-eu.getcensus.com",
                "password": "secret-token:workspace-token",
            },
        }

    def __init__(self, census_conn_id: str = default_conn_name, *args, **kwargs) -> None:
        super().__init__(http_conn_id=census_conn_id, *args, **kwargs)
        self.census_conn_id = census_conn_id

    def _get_secret_token(self) -> str:
        conn = self.get_connection(self.http_conn_id)
        secret_token = conn.password
        if not secret_token:
            raise AirflowException("An Activations API token is required for this hook.")
        return secret_token

    def get_api_base_url(self) -> str:
        conn = self.get_connection(self.census_conn_id)
        host = (conn.host or "app.getcensus.com").rstrip("/")
        if host.startswith(("http://", "https://")):
            return host
        return f"https://{host}"

    def get_auth_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._get_secret_token()}"}

    def get_sync_history_url(self, sync_id: int, sync_run_id: int | str | None = None) -> str:
        url = f"{self.get_api_base_url()}/syncs/{sync_id}/history"
        if sync_run_id is None:
            return url
        return f"{url}?sync_run_id={sync_run_id}"

    def get_conn(self, headers=None, extra_options=None) -> requests.Session:
        auth_headers = self.get_auth_headers()
        all_headers = {**auth_headers, **headers} if headers else auth_headers

        session = super().get_conn(all_headers, extra_options)
        self.base_url = self.get_api_base_url()

        return session

    def trigger_sync(self, sync_id: int) -> int:
        endpoint = "api/v1/syncs/{sync_id}/trigger".format(sync_id=sync_id)

        self.method = "POST"
        response = self.run(endpoint)
        response.raise_for_status()

        return response.json()["data"]["sync_run_id"]

    def get_sync_run_info(self, sync_run_id: int | str) -> Dict[str, Any]:
        endpoint = "api/v1/sync_runs/{sync_run_id}".format(sync_run_id=sync_run_id)

        self.method = "GET"
        response = self.run(endpoint)
        response.raise_for_status()

        return response.json()["data"]

    def test_connection(self) -> tuple[bool, str]:
        self.method = "GET"

        try:
            response = self.run("api/v1/syncs?page=1&per_page=1")
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            return False, f"Unable to connect to Census Activations API: {exc}"

        if payload.get("status") != "success":
            return False, "Unexpected response from Census Activations API."

        return True, "Connection successfully tested against Census Activations API."

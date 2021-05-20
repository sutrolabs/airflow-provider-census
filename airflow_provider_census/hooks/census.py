try:
    # airflow 2.0
    from airflow.providers.http.hooks.http import HttpHook
except ImportError:
    # airflow 1.10
    from airflow.hooks.http_hook import HttpHook

from airflow.exceptions import AirflowException
import requests
from typing import Any, Dict

class CensusHook(HttpHook):
    '''
    Census API hook

    :param census_conn_id: `Conn ID` of the Connection to be used to configure this hook.
    :type census_conn_id: str
    '''

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        return {
            'hidden_fields': ['login'],
            'relabeling': {
                'password': 'Census Secret Token'
            }
        }

    def __init__(self, census_conn_id: str = 'census_default', *args, **kwargs) -> None:
        super().__init__(http_conn_id = census_conn_id, *args, **kwargs)

    def _get_secret_token(self) -> str:
        conn = self.get_connection(self.http_conn_id)
        secret_token = conn.password
        if not secret_token:
            raise AirflowException('Census Secret Token is required for this hook.')
        return secret_token

    def get_conn(self, headers) -> requests.Session:
        secret_token = self._get_secret_token()

        auth_header = {
            'Authorization': f'Bearer {secret_token}'
        }

        all_headers = {**auth_header, **headers} if headers else auth_header

        session = super().get_conn(all_headers)
        return session
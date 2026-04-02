from unittest.mock import patch

from airflow_provider_census.links.census import CensusSyncRunLink
from airflow_provider_census.operators.census import CensusOperator


class DummyTaskInstanceKey:
    run_id = "manual__2026-04-01T00:00:00+00:00"


class TestCensusSyncRunLink:
    def test_get_link_uses_sync_history_url(self):
        operator = CensusOperator(sync_id=42, task_id="census_operator")
        link = CensusSyncRunLink()

        with patch("airflow_provider_census.links.census.XCom.get_value", return_value=99), patch(
            "airflow_provider_census.links.census.CensusHook.get_sync_history_url",
            return_value="https://app.getcensus.com/syncs/42/history?sync_run_id=99",
        ):
            assert (
                link.get_link(operator, ti_key=DummyTaskInstanceKey())
                == "https://app.getcensus.com/syncs/42/history?sync_run_id=99"
            )

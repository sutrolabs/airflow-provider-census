from airflow.exceptions import AirflowException
import pytest

from airflow_provider_census.sensors.census import CensusSensor
from airflow_provider_census.triggers.census import CensusTrigger


class DeferCalled(Exception):
    pass


class TestCensusSensor:
    def test_poke_working(self, requests_mock):
        sync_run_info_json = {
            "status": "success",
            "data": {
                "status": "working",
            },
        }
        requests_mock.get("https://app.getcensus.com/api/v1/sync_runs/0", json=sync_run_info_json)

        sensor = CensusSensor(sync_run_id=0, task_id="census_sensor")

        assert not sensor.poke(None)

    def test_poke_failed(self, requests_mock):
        sync_run_info_json = {
            "status": "success",
            "data": {
                "error_message": "something broke",
                "status": "failed",
            },
        }
        requests_mock.get("https://app.getcensus.com/api/v1/sync_runs/0", json=sync_run_info_json)

        sensor = CensusSensor(sync_run_id=0, task_id="census_sensor")

        with pytest.raises(AirflowException) as excinfo:
            sensor.poke(None)

        assert str(excinfo.value) == "Census sync run 0 failed with error: something broke"

    def test_poke_completed(self, requests_mock):
        sync_run_info_json = {
            "status": "success",
            "data": {
                "status": "completed",
            },
        }
        requests_mock.get("https://app.getcensus.com/api/v1/sync_runs/0", json=sync_run_info_json)

        sensor = CensusSensor(sync_run_id=0, task_id="census_sensor")

        assert sensor.poke(None)

    def test_execute_deferrable_defers(self, monkeypatch):
        sensor = CensusSensor(sync_run_id=7, task_id="census_sensor", deferrable=True, poke_interval=42)
        captured = {}

        monkeypatch.setattr(sensor, "poke", lambda context: False)

        def fake_defer(*, trigger, method_name):
            captured["trigger"] = trigger
            captured["method_name"] = method_name
            raise DeferCalled

        monkeypatch.setattr(sensor, "defer", fake_defer)

        with pytest.raises(DeferCalled):
            sensor.execute(None)

        assert isinstance(captured["trigger"], CensusTrigger)
        assert captured["trigger"].sync_run_id == 7
        assert captured["trigger"].poll_interval == 42.0
        assert captured["method_name"] == "execute_complete"

    def test_execute_complete_failed(self):
        sensor = CensusSensor(sync_run_id=7, task_id="census_sensor", deferrable=True)

        with pytest.raises(AirflowException) as excinfo:
            sensor.execute_complete(
                None,
                {"sync_run_id": 7, "status": "failed", "error_message": "something broke"},
            )

        assert str(excinfo.value) == "Census sync run 7 failed with error: something broke"

    def test_execute_complete_completed(self):
        sensor = CensusSensor(sync_run_id=7, task_id="census_sensor", deferrable=True)

        assert sensor.execute_complete(None, {"sync_run_id": 7, "status": "completed"}) is None

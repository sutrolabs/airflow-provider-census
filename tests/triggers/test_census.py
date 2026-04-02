import asyncio

from airflow_provider_census.triggers.census import CensusTrigger


async def first_event(trigger):
    async for event in trigger.run():
        return event
    raise AssertionError("Trigger did not emit an event")


class TestCensusTrigger:
    def test_serialize(self):
        trigger = CensusTrigger(sync_run_id=7, census_conn_id="custom_census", poll_interval=15)

        assert trigger.serialize() == (
            "airflow_provider_census.triggers.census.CensusTrigger",
            {
                "sync_run_id": 7,
                "census_conn_id": "custom_census",
                "poll_interval": 15.0,
            },
        )

    def test_run_emits_completed_event(self, monkeypatch):
        trigger = CensusTrigger(sync_run_id=7, poll_interval=0)

        async def fake_get_sync_run_info(**kwargs):
            return {"status": "completed"}

        monkeypatch.setattr(trigger, "_get_sync_run_info", fake_get_sync_run_info)

        event = asyncio.run(first_event(trigger))

        assert event.payload == {
            "sync_run_id": 7,
            "status": "completed",
            "error_message": None,
        }

import subprocess

from airflow import settings
from airflow.models.connection import Connection

CONN_ID = "census_default"


def pytest_sessionstart(session):
    subprocess.run(["airflow", "db", "migrate"], check=True)

    db_session = settings.Session()
    db_session.query(Connection).filter(Connection.conn_id == CONN_ID).delete()
    db_session.add(
        Connection(
            conn_id=CONN_ID,
            conn_type="census",
            password="secret-token:census",
        )
    )
    db_session.commit()
    db_session.close()


def pytest_sessionfinish(session, exitstatus):
    db_session = settings.Session()
    db_session.query(Connection).filter(Connection.conn_id == CONN_ID).delete()
    db_session.commit()
    db_session.close()

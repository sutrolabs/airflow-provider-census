from airflow import settings
from airflow.models import Connection
import os

def pytest_sessionstart(session):
    os.system('poetry run airflow db init')

    global conn
    conn = Connection(
        conn_id = 'census_default',
        conn_type = 'Census',
        password = 'secret-token:census'
    )

    session = settings.Session()
    session.add(conn)
    session.commit()


def pytest_sessionfinish(session, exitstatus):
    global conn
    session = settings.Session()
    session.delete(conn)
    session.commit()

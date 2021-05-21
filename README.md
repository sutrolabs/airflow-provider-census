# Census Provider for Apache Airflow

This package allows you to trigger syncs for [Census](https://www.getcensus.com/).

## Installation

Install the [airflow-provider-census](https://pypi.org/project/airflow-provider-census/) package from PyPI using your preferred way of installing python packages.

## Configuration

There are 2 ways to configure a Census connection depending on whether you are using Airflow 1.10 or Airflow 2.

The `CensusHook` and `CensusOperator` use the `census_default` connection id as a default, although this is configurable if you would like to use your own connection id.

### Configuration in Airflow 1.10

In the Airflow Connections UI, create a new connection:

* Conn ID: census_default
* Conn Type: HTTP
* Password: secret-token

### Configuration in Airflow 2

In the Airflow Connections UI, create a new connection:

* Conn Id: census_default
* Conn Type: Census
* Census Secret Token: secret-token

## Hooks

### CensusHook

`CensusHook` is a class that inherits from `HttpHook` and can be used to run http requests for Census.
You will most likely interact with the operator rather than the hook.

The hook can be imported by the following code:

```python
from airflow_provider_census.hooks.census import CensusHook
```

### CensusOperator

`CensusOperator` triggers a sync job in Census. The operator takes 2 parameters:

1. sync_id : Navigate to the sync and check the url for the sync id. This should be a required integer.
2. census_conn_id: The connection id to use. This is optional and defaults to 'census_default'.

The operator can be imported by the following code:

```python
from airflow_provider_census.operators.census import CensusOperator
```

## Example

The following example will run a Census sync once a day:

```python
from airflow_provider_census.operators.census import CensusOperator

from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1)
}

dag = DAG('census', default_args = default_args)

sync = CensusOperator(sync_id = 27, dag = dag, task_id = 'sync')
```

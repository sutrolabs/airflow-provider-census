# Census Provider for Apache Airflow

This package allows you to trigger syncs for [Census](https://www.getcensus.com/).

## Installation

Install the [airflow-provider-census](https://pypi.org/project/airflow-provider-census/) package from PyPI using your preferred way of installing python packages.

## Configuration

There are 2 ways to configure a Census connection depending on whether you are using Airflow 1.10 or Airflow 2.

The `CensusHook` and `CensusOperator` use the `census_default` connection id as a default, although this is configurable if you would like to use your own connection id.

### Finding the secret-token

1. Go to any sync at https://app.getcensus.com/syncs
2. Click on the Sync Configuration tab.
3. Next to API TRIGGER, click "Click to show"
4. The url will be of the format https://bearer:secret-token:arandomstring@app.getcensus.com/api/v1/syncs/0/trigger
5. the secret token will be of the format "secret-token:arandomstring" in the url above, including the "secret-token:" part. Do not include the "@".

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

## Operators

### CensusOperator

`CensusOperator` triggers a sync job in Census. The operator takes the following parameters:

1. sync_id : Navigate to the sync and check the url for the sync id. For example https://app.getcensus.com/syncs/0/overview here, the sync_id would be 0.
2. census_conn_id : The connection id to use. This is optional and defaults to 'census_default'.

The operator can be imported by the following code:

```python
from airflow_provider_census.operators.census import CensusOperator
```

## Sensors

### CensusSensor

`CensusSensor` polls a sync run in Census. The sensor takes the following parameters:

1. sync_run_id : The sync run id you get back from the CensusOperator which triggers a new sync.
2. census_conn_id : The connection id to use. This is optional and defaults to 'census_default'.

The sensor can be imported by the following code:

```python
from airflow_provider_census.sensors.census import CensusSensor
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

sensor = CensusSensor(sync_run_id = "{{ ti.xcom_pull(task_ids = 'sync') }}", dag = dag, task_id = 'sensor')

sync >> sensor
```

# Feedback

[Source code available on Github](https://github.com/sutrolabs/airflow-provider-census). Feedback and pull requests are greatly appreciated. Let us know if we can improve this.


# From

:wave: The folks at [Census](http://getcensus.com) originally put this together. Have data? We'll sync your data warehouse with your CRM and the customer success apps critical to your team.

# Need help setting this up?

You can always contact us via support@getcensus.com or [in-app](https://app.getcensus.com/) via the live chat in the bottom right corner.

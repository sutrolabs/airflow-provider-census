def get_provider_info():
    return {
        "package-name": "airflow-provider-census",
        "name": "Fivetran Activations Provider",
        "description": "A Fivetran Activations provider for Apache Airflow.",
        "integrations": [
            {
                "integration-name": "Fivetran Activations",
                "external-doc-url": "https://fivetran.com/docs/activations/rest-api/api-reference/introduction",
            }
        ],
        "hooks": [
            {
                "integration-name": "Fivetran Activations",
                "python-modules": ["airflow_provider_census.hooks.census"],
            }
        ],
        "operators": [
            {
                "integration-name": "Fivetran Activations",
                "python-modules": ["airflow_provider_census.operators.census"],
            }
        ],
        "sensors": [
            {
                "integration-name": "Fivetran Activations",
                "python-modules": ["airflow_provider_census.sensors.census"],
            }
        ],
        "triggers": [
            {
                "integration-name": "Fivetran Activations",
                "python-modules": ["airflow_provider_census.triggers.census"],
            }
        ],
        "connection-types": [
            {
                "hook-class-name": "airflow_provider_census.hooks.census.CensusHook",
                "connection-type": "census",
            }
        ],
        "extra-links": ["airflow_provider_census.links.census.CensusSyncRunLink"],
        "versions": ["2.1.0"],
    }

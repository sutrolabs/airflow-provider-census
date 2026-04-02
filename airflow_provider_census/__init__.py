def get_provider_info():
    return {
        "package-name": "airflow-provider-census",
        "name": "Census Provider",
        "description": "A Census provider for Apache Airflow.",
        "integrations": [
            {
                "integration-name": "Census",
                "external-doc-url": "https://fivetran.com/docs/activations/rest-api/api-reference/introduction",
            }
        ],
        "hooks": [
            {
                "integration-name": "Census",
                "python-modules": ["airflow_provider_census.hooks.census"],
            }
        ],
        "operators": [
            {
                "integration-name": "Census",
                "python-modules": ["airflow_provider_census.operators.census"],
            }
        ],
        "sensors": [
            {
                "integration-name": "Census",
                "python-modules": ["airflow_provider_census.sensors.census"],
            }
        ],
        "triggers": [
            {
                "integration-name": "Census",
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

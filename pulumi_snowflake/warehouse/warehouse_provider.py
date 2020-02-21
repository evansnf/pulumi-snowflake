from pulumi_snowflake import Client

from ..baseprovider import BaseDynamicProvider
from ..provider import Provider


class WarehouseProvider(BaseDynamicProvider):
    """
    Dynamic provider for Snowflake Warehouse resources.
    """

    def __init__(self, provider_params: Provider, connection_provider: Client):
        super().__init__(provider_params, connection_provider)

    def generate_sql_create_statement(self, validated_name, inputs, environment):
        template = environment.from_string(
"""CREATE WAREHOUSE {{ full_name }}
{% if warehouse_size %}WAREHOUSE_SIZE = {{ warehouse_size | sql }}
{% endif %}
{%- if max_cluster_count %}MAX_CLUSTER_COUNT = {{ max_cluster_count | sql }}
{% endif %}
{%- if min_cluster_count %}MIN_CLUSTER_COUNT = {{ min_cluster_count | sql }}
{% endif %}
{%- if scaling_policy %}SCALING_POLICY = {{ scaling_policy | sql }}
{% endif %}
{%- if auto_suspend %}AUTO_SUSPEND = {{ auto_suspend | sql }}
{% endif %}
{%- if auto_resume %}AUTO_RESUME = {{ auto_resume | sql }}
{% endif %}
{%- if initially_suspended %}INITIALLY_SUSPENDED = {{ initially_suspended | sql }}
{% endif %}
{%- if comment %}COMMENT = {{ comment | sql }}
{% endif %}""")

        sql = template.render({
            "full_name": self._get_full_object_name(inputs, validated_name),
            **inputs
        })

        return sql

    def generate_sql_drop_statement(self, validated_name, inputs, environment):
        template = environment.from_string("DROP WAREHOUSE {{ full_name }}")
        sql = template.render({
            "full_name": self._get_full_object_name(inputs, validated_name)
        })
        return sql
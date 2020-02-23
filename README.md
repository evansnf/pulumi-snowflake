# pulumi-snowflake

This project contains a pip packaged named `pulumi-snowflake` which allows Snowflake resources to be managed in Pulumi.

> **NOTE:** This package relies on the `snowflake-connector-python` pip package, which has specific setup instructions.  [Please ensure you check the prerequesits for your platform](https://docs.snowflake.net/manuals/user-guide/python-connector-install.html) before using the `pulumi-snowflake` package.

An example Pulumi program which uses this package is present in the `example` folder.

## Prerequesits

* Install the package into your Pulumi project using `pip`
* Set your Snowflake credentials in your stack config:

```
pulumi config set snowflakeAccountName [snowflake account name]
pulumi config set --secret snowflakeUsername [snowflake username]
pulumi config set --secret snowflakePassword [snowflake password]
pulumi config set --secret snowflakeRole [snowflake role]
```

> Note: `snowflakeRole` is optional.

## Resources

Currently this package supports the following resources:

* The `pulumi_snowflake.fileformat.FileFormat` class is a Pulumi resource for managing [Snowflake file format objects](https://docs.snowflake.net/manuals/sql-reference/sql/create-file-format.html).
* The `pulumi_snowflake.storage_integration.AWSStorageIntegration` class is a Pulumi resource for managing [storage integration objects with AWS parameters](https://docs.snowflake.net/manuals/sql-reference/sql/create-storage-integration.html).
* The `pulumi_snowflake.stage.Stage` class is a Pulumi resource for managing [Snowflake staging areas](https://docs.snowflake.net/manuals/sql-reference/sql/create-stage.html)
* The `pulumi_snowflake.database.Database` class is a Pulumi resource for managing [Snowflake databases](https://docs.snowflake.net/manuals/sql-reference/sql/create-database.html)
* The `pulumi_snowflake.schema.Schema` class is a Pulumi resource for managing [Snowflake schemas](https://docs.snowflake.net/manuals/sql-reference/sql/create-schema.html)
* The `pulumi_snowflake.warehouse.Warehouse` class is a Pulumi resource for managing [Snowflake warehouses](https://docs.snowflake.net/manuals/sql-reference/sql/create-warehouse.html)
* The `pulumi_snowflake.pipe.Pipe` class is a Pulumi resource for managing [Snowflake pipes](https://docs.snowflake.net/manuals/sql-reference/sql/create-pipe.html)

### Resource naming

By default, resource names in Snowflake are case-insensitive.  However, [if an identifier uses any special characters,
it must be enquoted](https://docs.snowflake.net/manuals/sql-reference/identifiers-syntax.html),
which makes it case-sensitive.  `pulumi-snowflake` will automatically enquote these
identifiers for you, but be aware that this will make them case-sensitive - for example, a resource with the name
`FooBar` can be referred to with any case, but an identifier with the name `Foo-Bar` (which contains a special character)
_must_ be referred to with the same case.

## Development

The directory structure is as follows:

```
├── example                     # An example of a Pulumi program using this package with AWS
├── pulumi_snowflake            # The main package source
│   ├── baseprovider            # The dynamic provider base class and related classes
│   ├── database                # The Database resource and dynamic provider
│   ├── fileformat              # The File Format resource and dynamic provider
│   ├── pipe                    # The Pipe resource and dynamic provider
│   ├── schema                  # The Schema resource and dynamic provider
│   ├── stage                   # The Stage resource and dynamic provider
│   ├── storageintegration      # The Storage Integration resource and dynamic provider
│   └── warehouse               # The Warehouse resource and dynamic provider
└── test                        # Unit tests
    ├── fileformat
    ├── provider
    ├── stage
    └── storageintegration
```

### Unit tests

* To run the unit tests (you may also want to instantiate a virtual environment in the root directory):

```
python setup.py test
```

### Generic object provider framework

The dynamic providers are built on top of a generic base class which makes it straightforward to support new object types in the future.  The `BaseDynamicProvider` class handles the `create`, `diff` and `delete` methods based on the Pulumi inputs it receives, and it delegates the generation of the actual SQL statements to the subclass by calling the `generate_sql_create_statement` and `generate_sql_drop_statement` methods.  These methods are usually implemented using Jinja templates.  As such, the base class also passes a Jinja environment into the subclass which adds a couple of useful filters for SQL value conversion:
* The `sql` filter, which automatically converts Python values to their SQL equivalent, assuming that all Python strings should become single-quoted SQL strings
* The `sql_identifier` filter, which converts a Python string explicitely to a SQL identifier.

For example, the Database object provider's `generate_sql_create_statement` is defined like so:

```python
def generate_sql_create_statement(self, validated_name, inputs, environment):
    template = environment.from_string(
"""CREATE{% if transient %} TRANSIENT{% endif %} DATABASE {{ full_name }}
{% if share %}FROM SHARE {{ share | sql_identifier }}
{% endif %}
{%- if data_retention_time_in_days %}DATA_RETENTION_TIME_IN_DAYS = {{ data_retention_time_in_days | sql }}
{% endif %}
{%- if comment %}COMMENT = {{ comment | sql }}
{% endif %}
""")

    sql = template.render({
        "full_name": self._get_full_object_name(inputs, validated_name),
        **inputs
    })

    return sql
```
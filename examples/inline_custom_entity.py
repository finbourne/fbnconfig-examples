from fbnconfig import Deployment, customentity, datatype, lumi
from fbnconfig import property as prop
from fbnconfig.inline_customentity import CustomEntityInlineResource
from fbnconfig.properties import MetricValue, PropertyValue

"""
An example configuration for defining a Custom Entity with inlined properties.

Creates:
- A Custom Entity type with a field
- An identifier property definition for the entity
- A currency property definition (currencyAndAmount type)
- Inlined properties that configure the Luminesce provider columns,
  including nested fields for the currency property (Amount and Currency)
- A Custom Entity instance with property values to verify the inlined view

This demonstrates how to set up a Custom Entity that is queryable via
Luminesce with identifier columns and structured property sub-fields
inlined into the provider.

After this is run:

select DisplayName, Status, [External ID], [Price Amount], [Price Currency], identifiers
  from [Lusid.CustomEntity.fbnconfig_ce_inline_example]
;

Should give:

+-------------+--------+------------+--------+-----+----------------------------------------
| DisplayName | Status | External ID| Amount | Ccy | Identifiers
+-------------+--------+------------+--------+-----+----------------------------------------
| Test Widget | Active | WIDGET-001 |  99.95 | GBP | CustomEntity/.../ExternalId=WIDGET-001
+-------------+--------+------------+--------+-----+----------------------------------------

"""


def configure(env):
    deployment_name = getattr(env, "name", "fbnconfig_ce_inline_example")
    # Define the custom entity type with a field
    entity_type = customentity.EntityTypeResource(
        id="example-ce-type",
        entity_type_name=deployment_name,
        display_name="Example Entity",
        description="A custom entity with inlined properties",
        field_schema=[
            customentity.FieldDefinition(
                name="Status",
                lifetime=customentity.LifeTime.PERPETUAL,
                type=customentity.FieldType.STRING,
                required=False,
            ),
        ],
    )
    # Shared data type references
    string_type = datatype.DataTypeRef(
        id="systemstring", scope="system", code="string",
    )
    ccy_type = datatype.DataTypeRef(
        id="systemccy", scope="system", code="currencyAndAmount",
    )
    # Define an identifier property for the entity
    identifier_prop = prop.DefinitionResource(
        id="example-ce-identifier",
        domain=prop.Domain.CustomEntity,
        scope=deployment_name,
        code="ExternalId",
        display_name="External ID",
        data_type_id=string_type,
        life_time=prop.LifeTime.Perpetual,
        constraint_style=prop.ConstraintStyle.Identifier,
    )
    # Define a currencyAndAmount property for the entity
    price_prop = prop.DefinitionResource(
        id="example-ce-price",
        domain=prop.Domain.CustomEntity,
        scope=deployment_name,
        code="Price",
        display_name="Price",
        data_type_id=ccy_type,
        life_time=prop.LifeTime.Perpetual,
    )
    # Inline properties into the Luminesce provider
    inline = CustomEntityInlineResource(
        id="example-ce-inline",
        custom_entity_type=entity_type,
        properties=[
            # Identifier column (key only, no field)
            lumi.InlineProperty(
                key=identifier_prop,
                name="External ID",
                description="External identifier for the entity",
            ),
            # Nested fields for currencyAndAmount: .Value and .Unit
            lumi.InlineProperty(
                key=price_prop,
                field="Value",
                name="Price Amount",
                data_type=lumi.InlineDataType.Decimal,
                description="The amount of the price",
            ),
            lumi.InlineProperty(
                key=price_prop,
                field="Unit",
                name="Price Currency",
                data_type=lumi.InlineDataType.Text,
                description="The currency of the price",
            ),
        ],
    )
    # Create a custom entity instance to verify the inlined view
    entity_instance = customentity.EntityResource(
        id="example-ce-instance",
        entity_type=entity_type,
        display_name="Test Widget",
        description="An example entity instance",
        identifiers=[
            customentity.EntityIdentifier(
                identifier_type=identifier_prop,
                identifier_value="WIDGET-001",
            ),
        ],
        fields=[
            customentity.EntityField(name="Status", value="Active"),
        ],
        properties=[
            PropertyValue(
                property_key=price_prop,
                metric_value=MetricValue(value=99.95, unit="GBP"),
            ),
        ],
    )
    # add everything to the deployment
    return Deployment(
        deployment_name,
        [entity_type, identifier_prop, price_prop, inline, entity_instance],
    )

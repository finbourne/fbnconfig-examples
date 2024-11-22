from fbnconfig import customentity
from fbnconfig import Deployment

"""
An example configuration for a custom entity.
The script configures the following entities:
- Entity Type

More information can be found here:
https://support.lusid.com/knowledgebase/article/KA-01750/en-us
"""


def configure(env):
    ce = customentity.EntityTypeResource(
        id="ce1",
        entityTypeName="entity-type-name",
        displayName="Example Custom Entity",
        description="An example custom entity",
        fieldSchema=[
            customentity.FieldDefinition(
                name="Field1",
                lifetime=customentity.LifeTime.Perpetual,
                type=customentity.FieldType.String,
                collectionType=customentity.CollectionType.Single,
                required=True,
            ),
            customentity.FieldDefinition(
                name="Field2",
                lifetime=customentity.LifeTime.TimeVariant,
                type=customentity.FieldType.String,
                required=True,
            ),
        ],
    )
    return Deployment("custom_entity_example", [ce])

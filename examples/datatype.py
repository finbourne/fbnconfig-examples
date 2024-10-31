from fbnconfig import property
from fbnconfig import datatype
from fbnconfig import Deployment

"""
An example configuration for data types.
The script configures the following entities:
- Data type

More information can be found here:
https://support.lusid.com/knowledgebase/article/KA-01743/
"""


def configure():
    strategy_type = datatype.DataTypeResource(
        id="datatype-example",
        scope="sc1",
        code="cd1",
        typeValueRange=datatype.TypeValueRange.Closed,
        displayName="Portfolio Strategy Test",
        description="A test datatype modified",
        valueType=datatype.ValueType.String,
        referenceData=datatype.ReferenceData(
            fieldDefinitions=[
                datatype.FieldDefinition(key="description", isRequired=True, isUnique=False),
                datatype.FieldDefinition(key="commission", isRequired=True, isUnique=False),
            ],
            values=[
                datatype.FieldValue(
                    value="I", fields={"description": "Investment Portfolio", "commission": "0.01"}
                ),
                datatype.FieldValue(
                    value="H", fields={"description": "Hedging Portfolio", "commission": "0.05"}
                ),
                datatype.FieldValue(
                    value="C", fields={"description": "Client Portfolio", "commission": "0.10"}
                ),
            ],
        ),
    )

    strategy_prop = property.DefinitionResource(
        id="strategy-property",
        domain=property.Domain.Portfolio,
        scope="sc1",
        code="strategy",
        displayName="Example portfolio strategy",
        dataTypeId=strategy_type,
        constraintStyle=property.ConstraintStyle.Property,
        propertyDescription="Example strategy datatype property",
        lifeTime=property.LifeTime.Perpetual,
    )

    priority_type = datatype.DataTypeResource(
        id="priority",
        scope="sc1",
        code="priority",
        typeValueRange=datatype.TypeValueRange.Closed,
        displayName="Priority datatype example",
        description="A datatype for Priority values",
        valueType=datatype.ValueType.String,
        acceptableValues=["High", "Medium", "Low"],
    )

    return Deployment("datatype_example", [strategy_type, strategy_prop, priority_type])

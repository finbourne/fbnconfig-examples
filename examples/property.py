from fbnconfig import property
from fbnconfig import datatype
from fbnconfig import Deployment

"""
An example configuration for defining property related entities.
The script configures the following entities:
- Property definition


More information can be found here:
https://support.lusid.com/knowledgebase/article/KA-01855/
"""


def configure(env):
    dom_ccy = property.DefinitionRef(
        id="dfdomccy", domain=property.Domain.Holding, scope="default", code="DfDomCcy"
    )

    nominal = property.DefinitionRef(
        id="nominal", domain=property.Domain.Holding, scope="default", code="Nominal"
    )

    rating = property.DefinitionResource(
        id="rating",
        domain=property.Domain.Instrument,
        scope="sc1",
        code="rating",
        displayName="Rating",
        dataTypeId=datatype.DataTypeRef(id="default_str", scope="system", code="string"),
        constraintStyle=property.ConstraintStyle.Collection,
        propertyDescription="Example property representing a rating",
        lifeTime=property.LifeTime.Perpetual,
        collectionType=property.CollectionType.Array,
    )

    instrument_property_definition = property.DefinitionResource(
        id="pd1",
        domain=property.Domain.Instrument,
        scope="sc1",
        code="pd1",
        displayName="Property definition example",
        dataTypeId=property.ResourceId(scope="system", code="number"),
        constraintStyle=property.ConstraintStyle.Property,
        propertyDescription="Example property definition",
        lifeTime=property.LifeTime.Perpetual,
        collectionType=None,
    )

    pv_nominal = property.DefinitionResource(
        id="derived",
        domain=property.Domain.Holding,
        dataTypeId=property.ResourceId(scope="system", code="number"),
        scope="sc1",
        code="PVNominal",
        propertyDescription="Example derived property",
        displayName="DF Nominal",
        derivationFormula=property.Formula("{x} * {y}", x=dom_ccy, y=nominal),
    )

    derived_property = property.DefinitionResource(
        id="derived_property",
        domain=property.Domain.Holding,
        dataTypeId=property.ResourceId(scope="system", code="number"),
        scope="sc1",
        code="derived_property",
        propertyDescription="pd1 x df x nominal",
        displayName="DF Nominal pd1",
        derivationFormula=property.Formula("{x} * {y}", x=pv_nominal, y=instrument_property_definition),
    )

    return Deployment(
        "property_example",
        [instrument_property_definition, dom_ccy, nominal, pv_nominal, derived_property, rating],
    )

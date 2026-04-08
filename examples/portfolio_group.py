import datetime as dt

from fbnconfig import Deployment, datatype, portfolio, portfolio_group, property
from fbnconfig.properties import PropertyValue


def configure(_):
    start_date = dt.date(2024, 1, 5)
    scope = "robtest-batch"
    portfolios = [
        portfolio.PortfolioResource(
            id=f"portfolio_{id}",
            scope=scope,
            code=f"qq_{id}",
            display_name=f"portfolio {id}",
            description=f"Batch Test Portfolio {id}",
            created=start_date,
            base_currency="USD",
            instrument_scopes=[scope],
        )
        for id in range(1, 4)
    ]
    group = portfolio_group.PortfolioGroupResource(
        id="group_1",
        scope=scope,
        created=start_date,
        code="gppp_1",
        display_name="Group 1",
        description="Batch Test Group 1",
        portfolios=portfolios,
    )
    string = datatype.DataTypeRef(id="datatype_string", scope="system", code="string")
    rating_prop = property.DefinitionResource(
        id="rating_prop", scope=scope, code="rating",
        domain=property.Domain.PortfolioGroup,
        display_name="Rating", data_type_id=string,
    )
    group_props = portfolio_group.PortfolioGroupPropertiesResource(
        id="group_1_props", portfolio_group=group,
        properties=[PropertyValue(property_key=rating_prop, label_value="AAA")],
    )
    return Deployment("test-portfolio-groups", portfolios + [group, rating_prop, group_props])

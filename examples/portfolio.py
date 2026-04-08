import datetime as dt

from fbnconfig import Deployment, corporate_action, datatype, portfolio, property
from fbnconfig.properties import PropertyValue


def configure(_):
    start_date = dt.date(2024, 1, 5)
    scope = "fbnconfig-portfolio-example"
    string = datatype.DataTypeRef(
        id="datatype_string",
        scope="system",
        code="string",
    )
    test_property = property.DefinitionResource(
        id="test_property",
        scope=scope,
        code="portfolio_example",
        domain=property.Domain.Transaction,
        display_name="Portfolio Example Property",
        data_type_id=string,
    )
    rating_prop = property.DefinitionResource(
        id="rating_prop",
        scope=scope,
        code="rating",
        domain=property.Domain.Portfolio,
        display_name="Rating",
        data_type_id=string,
    )
    ca_source = corporate_action.CorporateActionSourceResource(
        id="ca_source",
        scope=scope,
        code="default-source",
        display_name="Default Corporate Action Source",
        instrument_scopes=[scope],
    )
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
            sub_holding_keys=[test_property],
            transaction_type_scope="default",
            transaction_type_source="alt1",
            corporate_action_source_id=ca_source,
        )
        for id in range(1, 4)
    ]
    portfolio_props = portfolio.PortfolioPropertiesResource(
        id="portfolio_1_props",
        portfolio=portfolios[0],
        properties=[PropertyValue(property_key=rating_prop, label_value="AAA")],
    )
    return Deployment("test-portfolios", [ca_source] + portfolios + [portfolio_props])

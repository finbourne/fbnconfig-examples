import datetime as dt

from fbnconfig import Deployment, datatype, portfolio, property
from fbnconfig import reference_portfolio as rp
from fbnconfig.properties import PropertyValue


def configure(_):
    scope = "fbnconfig-refportfolio-example"
    start_date = dt.date(2024, 1, 5)
    string = datatype.DataTypeRef(
        id="datatype_string",
        scope="system",
        code="string",
    )
    rating_prop = property.DefinitionResource(
        id="rating_prop",
        scope=scope,
        code="rating",
        domain=property.Domain.Portfolio,
        display_name="Rating",
        data_type_id=string,
    )
    portfolio_obj = rp.ReferencePortfolioResource(
        id="ref_portfolio",
        scope=scope,
        code="ref_pf",
        display_name="Reference Portfolio",
        description="A benchmark reference portfolio",
        base_currency="USD",
        created=start_date,
        instrument_scopes=["default"],
    )
    portfolio_props = portfolio.PortfolioPropertiesResource(
        id="ref_portfolio_props",
        portfolio=portfolio_obj,
        properties=[PropertyValue(property_key=rating_prop, label_value="AAA")],
    )
    constituents = rp.ReferencePortfolioConstituentsResource(
        id="ref_constituents",
        portfolio=portfolio_obj,
        effective_from=start_date,
        weight_type="Static",
        constituents=[
            rp.Constituent(
                instrument_identifiers={"Instrument/default/Currency": "USD"},
                weight=0.6,
                currency="USD",
            ),
            rp.Constituent(
                instrument_identifiers={"Instrument/default/Currency": "GBP"},
                weight=0.4,
                currency="GBP",
            ),
        ],
    )
    return Deployment("test-reference-portfolios", [
        portfolio_obj, rating_prop, portfolio_props, constituents,
    ])

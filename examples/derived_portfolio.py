import datetime as dt

from fbnconfig import Deployment, portfolio


def configure(_):
    scope = "robtest-batch"
    start_date = dt.date(2024, 1, 5)
    parent = portfolio.PortfolioResource(
        id="parent_portfolio",
        scope=scope,
        code="parent_pf",
        display_name="Parent Portfolio",
        description="Parent transaction portfolio",
        base_currency="USD",
        created=start_date,
        instrument_scopes=[scope],
    )
    derived = portfolio.DerivedTransactionPortfolioResource(
        id="derived_portfolio",
        scope=scope,
        code="derived_pf",
        display_name="Derived Portfolio",
        description="Derived from parent for what-if analysis",
        parent_portfolio_id=parent,
        created=start_date,
        instrument_scopes=[scope],
    )
    return Deployment("test-derived-portfolios", [parent, derived])

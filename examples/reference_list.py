import datetime as dt

from fbnconfig import Deployment, portfolio
from fbnconfig import reference_list as rl


def configure(env):
    strlist1 = rl.ReferenceListResource(
        id="strlist1",
        scope="sc1",
        code="strlist1",
        name="strlist_name",
        tags=["tag1", "tag2"],
        reference_list=rl.StringList(
            values=["value1", "value2", "value3"],
        )
    )
    instrlist1 = rl.ReferenceListResource(
        id="instrlist1",
        scope="sc1",
        code="instrlist1",
        name="instrlist1",
        tags=["tag1", "tag2"],
        reference_list=rl.InstrumentList(
            values=[
                "CCY_USD",
            ]
        )
    )
    pf1 = portfolio.PortfolioResource(
        id="pf1",
        scope="sc1",
        code="example-portfolio",
        display_name="Example Portfolio",
        base_currency="USD",
        created=dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc),
        instrument_scopes=["sc1"],
    )
    pflist1 = rl.ReferenceListResource(
        id="pflist1",
        scope="sc1",
        code="pflist1",
        name="Portfolio ID List",
        reference_list=rl.PortfolioIdList(
            values=[pf1],
        )
    )
    return Deployment(
        "reference_list_example",
        [pf1, strlist1, instrlist1, pflist1],
    )

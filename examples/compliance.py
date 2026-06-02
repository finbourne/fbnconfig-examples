
import datetime as dt

from fbnconfig import Deployment
from fbnconfig import compliance as cp
from fbnconfig import portfolio_group as pg
from fbnconfig import property as pr


def configure(env):
    ccy = pr.DefinitionRef(
        id="prop_ccy",
        domain=pr.Domain.Instrument,
        scope="default",
        code="Currency",
    )
    template1 = cp.ComplianceTemplateResource(
        id="template1",
        scope="sc1",
        code="template1",
        tags=["tag1", "tag2"],
        description="This is the first compliance template",
        variations=[
            cp.ComplianceTemplateVariation(
                label="Variation1",
                description="This is the first variation of the template",
                outcome_description="This variation checks for specific conditions",
                steps=[
                    cp.BranchStep(
                        label="Branch-Step-1",
                        parameters=[
                            cp.ComplianceTemplateParameter(
                                name="param1",
                                description="Parameter for branch step",
                                type="string",
                            )
                        ]
                    ),
                ],
                referenced_group_label=None
            )
        ]
    )
    group1 = pg.PortfolioGroupResource(
        id="group1",
        scope="sc1",
        code="compliance-group",
        display_name="Compliance Example Group",
        description="Portfolio group for compliance example",
        created=dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc),
    )
    rule1 = cp.ComplianceRuleResource(
        id="rule1",
        scope="sc1",
        code="rule1",
        name="ExampleComplianceRule",
        description="This is an example compliance rule",
        active=True,
        template_id=template1,
        variation="Variation1",
        portfolio_group_id=group1,
        parameters={
            "Branch-Step-1.BranchingKey": cp.GroupBySelectorComplianceParameter(value="1"),
        },
        properties=[
            cp.PropertyListItem(
                key=ccy,
                value=cp.PropertyValue(
                    label_value="CHF",
                ),
            )
        ]
    )
    return Deployment("compliance_example", [group1, template1, rule1])

"""Example configuration for group reconciliation resources.

Creates two portfolios, a recipe, a ComparisonRuleset, and a Reconciliation
that ties them together.
"""
import datetime as dt

from fbnconfig import Deployment, portfolio, recipe, reconciliation


def configure(env):
    deployment_name = getattr(env, "name", "reconciliation_example")
    scope = deployment_name
    start_date = dt.date(2024, 1, 5)

    pf_left = portfolio.PortfolioResource(
        id="pf_left", scope=scope, code="pf_left",
        display_name="Left Portfolio",
        description="Source portfolio for reconciliation",
        base_currency="USD", created=start_date, instrument_scopes=[scope],
    )
    pf_right = portfolio.PortfolioResource(
        id="pf_right", scope=scope, code="pf_right",
        display_name="Right Portfolio",
        description="Target portfolio for reconciliation",
        base_currency="USD", created=start_date, instrument_scopes=[scope],
    )

    recon_recipe = recipe.RecipeResource(
        id="recon_recipe", scope=scope, code="recipe1",
        recipe={
            "market": {
                "marketRules": [],
                "suppliers": {},
                "options": {
                    "defaultSupplier": "Lusid",
                    "defaultInstrumentCodeType": "LusidInstrumentId",
                    "defaultScope": "default",
                },
            },
        },
    )

    holding_ruleset = reconciliation.ComparisonRulesetResource(
        id="holding_ruleset",
        scope=scope,
        code="holding_ruleset",
        display_name="Holding ruleset",
        reconciliation_type=reconciliation.ReconciliationType.HOLDING,
        core_attribute_rules=[
            reconciliation.CoreAttributeRule(
                left=reconciliation.AttributeRuleOperand(
                    key="Instrument/default/LusidInstrumentId", operation="Value",
                ),
                right=reconciliation.AttributeRuleOperand(
                    key="Instrument/default/LusidInstrumentId", operation="Value",
                ),
            ),
        ],
        aggregate_attribute_rules=[
            reconciliation.AggregateAttributeRule(
                left=reconciliation.AttributeRuleOperand(
                    key="Holding/default/Units", operation="Sum",
                ),
                right=reconciliation.AttributeRuleOperand(
                    key="Holding/default/Units", operation="Sum",
                ),
            ),
        ],
    )

    holding_reconciliation = reconciliation.ReconciliationResource(
        id="holding_reconciliation",
        scope=scope,
        code="holding_reconciliation",
        display_name="Holding reconciliation",
        portfolio_entity_ids=reconciliation.PortfolioEntityIds(
            left=[pf_left],
            right=[pf_right],
        ),
        comparison_ruleset_ids=reconciliation.ComparisonRulesetIds(
            holding_reconciliation=holding_ruleset,
        ),
        # Holding (and Valuation) rulesets require currencies + recipe_ids.
        currencies=reconciliation.ReconciliationCurrencies(left="USD", right="USD"),
        recipe_ids=reconciliation.ReconciliationRecipeIds(
            left=recon_recipe,
            right=recon_recipe,
        ),
    )

    return Deployment(
        deployment_name,
        [pf_left, pf_right, recon_recipe, holding_ruleset, holding_reconciliation],
    )

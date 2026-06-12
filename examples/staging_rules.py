"""Example: deploy a staging rule set against a dedicated custom entity type.

This example deliberately scopes the staging rules to a custom entity type
(`example_staging_entity`) rather than a built-in LUSID entity type like
`Portfolio` or `Instrument`. Staging rules affect every action against the
target entity type — pointing them at a foundational type can block other
deployments and tests in the same tenant, so a dedicated entity type is
safer for an example you're going to copy.

Supported entity types for staging are `Portfolio`, `Instrument`, `DataType`,
`PropertyDefinition`, or a custom entity type. To target a built-in type pass
the name as a string instead of a custom entity resource/ref.

A staging rule only matches when its `match_criteria.entity_attributes` clause
is set — without one the rule silently fails to match and requests go through
unstaged. Use `"True"` as a tautology to match every entity, or a filter
expression like `"id.scope eq 'US-Equities'"` to narrow it down.

The `requesting_user` / `deciding_user` filters reference LUSID **roles**
(`id.scope`/`id.code` on the role identity), not the requester's user id.
For example, `"id.scope eq 'LUSID_SYSTEM' and id.code eq 'lusid-administrator'"`
matches anyone holding the built-in admin role.

After deploying, you can verify staging fires by creating an instance of the
custom entity (e.g. via curl with an Okta JWT or the LUSID Python SDK):

    POST /api/api/customentities/~example_staging_entity
    {
      "identifiers": [{
        "identifierScope": "<your-scope>",
        "identifierType": "ceid",
        "identifierValue": "demo-1"
      }],
      "fields": [{"name": "note", "value": "hello"}],
      "displayName": "Demo instance",
      "description": "demo"
    }

The response will be `200 OK` with a body containing:

    "stagedModifications": {
      "countPending": 1,
      "hrefPending": "https://<host>/api/api/stagedmodifications/?filter=...",
      "idsPreviewed": ["<staged-modification-id>"]
    }

`countPending: 1` confirms the rule matched and the create is awaiting
approval rather than committing immediately. Approve or reject it via the
`/stagedmodifications/{id}/$approve` / `$reject` endpoints. The CE instance
itself is intentionally **not** part of this deployment — fbnconfig would
otherwise treat the staged-not-yet-committed entity as created state, and the
next run would diverge.
"""
from fbnconfig import Deployment, customentity, staging_rules


def configure(_):
    entity_type = customentity.EntityTypeResource(
        id="example_staging_entity",
        entity_type_name="example_staging_entity",
        display_name="Staging Rules Example Entity",
        description="Demo custom entity used by the staging rules example.",
        field_schema=[
            customentity.FieldDefinition(
                name="note",
                lifetime=customentity.LifeTime.PERPETUAL,
                type=customentity.FieldType.STRING,
                required=False,
            ),
        ],
    )
    rule_set = staging_rules.StagingRuleSetResource(
        id="example_staging_rules",
        entity_type=entity_type,
        display_name="Example Staging Rules",
        description="Approval gates for the example entity.",
        rules=[
            staging_rules.StagingRule(
                rule_id="require-admin-approval-on-create",
                description=(
                    "Every Create against this entity type must be approved by"
                    " the lusid-administrator role. The staging user cannot"
                    " self-approve."
                ),
                status=staging_rules.StagingRuleStatus.ACTIVE,
                match_criteria=staging_rules.StagingRuleMatchCriteria(
                    action_in=["Create"],
                    entity_attributes="True",
                ),
                approval_criteria=staging_rules.StagingRuleApprovalCriteria(
                    required_approvals=1,
                    deciding_user=(
                        "id.scope eq 'LUSID_SYSTEM' and id.code eq"
                        " 'lusid-administrator'"
                    ),
                    staging_user_can_decide=False,
                ),
            ),
            staging_rules.StagingRule(
                rule_id="placeholder-inactive-delete-rule",
                description="Placeholder Delete rule, currently disabled.",
                status=staging_rules.StagingRuleStatus.INACTIVE,
                match_criteria=staging_rules.StagingRuleMatchCriteria(
                    action_in=["Delete"],
                    entity_attributes="True",
                ),
                approval_criteria=staging_rules.StagingRuleApprovalCriteria(
                    required_approvals=2,
                    deciding_user=(
                        "id.scope eq 'LUSID_SYSTEM' and id.code eq"
                        " 'lusid-administrator'"
                    ),
                    staging_user_can_decide=False,
                ),
            ),
        ],
    )
    return Deployment("example-staging-rules", [entity_type, rule_set])

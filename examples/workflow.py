from fbnconfig import Deployment
from fbnconfig import workflows as wf

"""
An example configuration for defining a Workflow with task definitions.

Creates a simple approval workflow:
- A root task definition with Pending -> InProgress -> Approved/Rejected states
- A review child task definition that is spawned during the approval process
- A Workflow entity that ties it all together via the root task definition
"""


def configure(env):
    deployment_name = getattr(env, "name", "fbnconfig_workflow_example")

    # Triggers
    start = wf.TriggerDefinition(name="Start", type="External")
    approve = wf.TriggerDefinition(name="Approve", type="External")
    reject = wf.TriggerDefinition(name="Reject", type="External")
    child_approved = wf.TriggerDefinition(name="ChildApproved", type="External")
    child_rejected = wf.TriggerDefinition(name="ChildRejected", type="External")

    # States
    pending = wf.TaskStateDefinition(name="Pending")
    in_review = wf.TaskStateDefinition(name="InReview")
    approved = wf.TaskStateDefinition(name="Approved")
    rejected = wf.TaskStateDefinition(name="Rejected")

    # Fields
    requester_field = wf.TaskFieldDefinition(
        name="Requester", type=wf.TaskFieldDefinitionType.STRING
    )
    reason_field = wf.TaskFieldDefinition(
        name="Reason", type=wf.TaskFieldDefinitionType.STRING
    )
    review_notes_field = wf.TaskFieldDefinition(
        name="ReviewNotes", type=wf.TaskFieldDefinitionType.STRING
    )

    # Child task: Review
    review_task_def = wf.TaskDefinitionResource(
        id="review-task-def",
        scope=deployment_name,
        code="ReviewRequest",
        display_name="Review Request",
        description="Review a submitted request and provide notes.",
        states=[pending, in_review, approved, rejected],
        field_schema=[requester_field, reason_field, review_notes_field],
        initial_state=wf.InitialState(
            name=pending, required_fields=[requester_field, reason_field]
        ),
        triggers=[start, approve, reject],
        transitions=[
            wf.TaskTransitionDefinition(
                from_state=pending, to_state=in_review, trigger=start
            ),
            wf.TaskTransitionDefinition(
                from_state=in_review,
                to_state=approved,
                trigger=approve,
                action=wf.ActionDefinition(
                    name="notify-parent-approved",
                    action_details=wf.TriggerParentTaskAction(trigger=child_approved),
                ),
            ),
            wf.TaskTransitionDefinition(
                from_state=in_review,
                to_state=rejected,
                trigger=reject,
                action=wf.ActionDefinition(
                    name="notify-parent-rejected",
                    action_details=wf.TriggerParentTaskAction(trigger=child_rejected),
                ),
            ),
        ],
        actions=[
            wf.ActionDefinition(
                name="notify-parent-approved",
                action_details=wf.TriggerParentTaskAction(trigger=child_approved),
            ),
            wf.ActionDefinition(
                name="notify-parent-rejected",
                action_details=wf.TriggerParentTaskAction(trigger=child_rejected),
            ),
        ],
    )

    # Action to create the review child task
    create_review_action = wf.ActionDefinition(
        name="create-review-task",
        action_details=wf.CreateChildTasksAction(
            child_task_configurations=[
                wf.ChildTaskConfiguration(
                    task_definition=review_task_def,
                    initial_trigger=start,
                    child_task_fields={
                        requester_field: wf.FieldMapping(map_from=requester_field),  # pyright: ignore
                        reason_field: wf.FieldMapping(map_from=reason_field),  # pyright: ignore
                    },
                )
            ]
        ),
    )

    # Root task definition: Approval
    root_task_def = wf.TaskDefinitionResource(
        id="approval-task-def",
        scope=deployment_name,
        code="ApprovalProcess",
        display_name="Approval Process",
        description="Root task for the approval workflow. Spawns a review child task.",
        states=[
            pending,
            wf.TaskStateDefinition(name="AwaitingReview"),
            approved,
            rejected,
        ],
        field_schema=[requester_field, reason_field],
        initial_state=wf.InitialState(
            name=pending, required_fields=[requester_field, reason_field]
        ),
        triggers=[start, child_approved, child_rejected],
        transitions=[
            wf.TaskTransitionDefinition(
                from_state=pending,
                to_state="AwaitingReview",
                trigger=start,
                action=create_review_action,
            ),
            wf.TaskTransitionDefinition(
                from_state="AwaitingReview",
                to_state=approved,
                trigger=child_approved,
            ),
            wf.TaskTransitionDefinition(
                from_state="AwaitingReview",
                to_state=rejected,
                trigger=child_rejected,
            ),
        ],
        actions=[create_review_action],
    )

    # Workflow entity tying it all together
    workflow = wf.WorkflowResource(
        id="approval-workflow",
        scope=deployment_name,
        code="ApprovalWorkflow",
        display_name="Approval Workflow",
        description="An approval workflow with a review child task.",
        root_task_definition=root_task_def,
    )

    return Deployment(deployment_name, [workflow])

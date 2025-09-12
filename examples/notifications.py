from fbnconfig import Deployment, notifications


def configure(env):
    deployment_name = getattr(env, "name", "subscriptions")

    basic_sub = notifications.SubscriptionResource(
        id="ExampleId",
        scope="sc1",
        code="cd1",
        display_name="Example display name",
        description="Example description",
        event_type="Manual",
        status=notifications.SubscriptionStatus.ACTIVE,
        filter="Body.subject eq 'TestEvent'"
    )
    return Deployment(deployment_name, [basic_sub])

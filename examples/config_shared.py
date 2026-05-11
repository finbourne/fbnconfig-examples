from fbnconfig import Deployment, configuration

"""
An example configuration for defining shared configuration sets and items.
The script configures the following entities:
- Configuration Set (shared)
- Configuration Item
"""


def configure(env):
    cs = configuration.SetResource(
        id="set1",
        scope="example",
        code="code4",
        type=configuration.SetType.SHARED,
        description="Example personal set resource",
    )
    username = configuration.ItemResource(
        id="user",
        set=cs,
        key="username",
        value="example-login",
        value_type=configuration.ValueType.TEXT,
        is_secret=False,
        description="Example key value pair representing a username",
    )
    passwd = configuration.ItemResource(
        id="password",
        set=cs,
        key="password",
        value="example-password",
        value_type=configuration.ValueType.TEXT,
        is_secret=False,
        description="Example key value pair representing a password",
    )
    set_ref = configuration.SetResource(
        id="set2",
        scope="example",
        code="code5",
        type=configuration.SetType.SHARED,
        description="Example shared set resource",
    )
    ins_item = configuration.ItemResource(
        id="username2",
        set=set_ref,
        key="user",
        value="example-login-2",
        value_type=configuration.ValueType.TEXT,
        is_secret=False,
        description="Example key value pair representing a username",
    )
    return Deployment("config_shared_example", [ins_item, cs, username, passwd])

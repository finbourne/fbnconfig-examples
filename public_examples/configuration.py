from fbnconfig import configuration
from fbnconfig import scheduler
from fbnconfig import Deployment

"""
An example configuration for defining configuration sets and their values.
The script configures the following entities:
- Configuration set
- Set item
- Image
- Job
- Schedule

The script configures an Image, Job and Schedule in order to show how you would
reference a configuration set item. For more information on these resources, see
`schedule.py` example.

More information can be found here:
https://support.lusid.com/knowledgebase/article/KA-01734/
https://support.lusid.com/knowledgebase/article/KA-01737/
https://support.lusid.com/knowledgebase/article/KA-01738/
"""


def configure():

    #
    # create a set and some items inside
    #
    cs = configuration.SetResource(
        id="set1",
        scope="sc1",
        code="cd1",
        type=configuration.SetType.PERSONAL,
        description="Example personal set resource",
    )

    username = configuration.ItemResource(
        id="user",
        set=cs,
        key="username",
        value="example-login",
        valueType=configuration.ValueType.TEXT,
        isSecret=False,
        description="Example key value pair representing a username",
    )

    passwd = configuration.ItemResource(
        id="password",
        set=cs,
        key="password",
        value="example-password",
        valueType=configuration.ValueType.TEXT,
        isSecret=False,
        description="Example key value pair representing a password",
    )

    #
    # add another set
    #
    setRef = configuration.SetResource(
        id="set2",
        scope="sc2",
        code="cd1",
        type=configuration.SetType.SHARED,
        description="Example shared set resource",
    )

    insItem = configuration.ItemResource(
        id="username2",
        set=setRef,
        key="user",
        value="example-login-2",
        valueType=configuration.ValueType.TEXT,
        isSecret=False,
        description="Example key value pair representing a username",
    )

    #
    # create a scheduler job that uses the config for username and leaves password empty
    #
    image = scheduler.ImageResource(
        id="img1",
        source_image="docker.io/alpine:latest",
        dest_name="example-image-name",
        dest_tag="latest",
    )

    job = scheduler.JobResource(
        id="job1",
        scope="sc1",
        code="example-job-name",
        image=image,
        name="example-job",
        description="Example of a job using a configuration item",
        minCpu="1",
        maxCpu="1",
        argumentDefinitions={
            "username": scheduler.EnvironmentArg(
                dataType="Configuration",
                required=False,
                description="A secret",
                order=1,
                defaultValue=username,
            ),
            "password": scheduler.EnvironmentArg(
                dataType="Configuration", required=False, description="A secret", order=1
            ),
        },
    )

    #
    # a schedule that uses config store for the password
    #
    schedule = scheduler.ScheduleResource(
        id="sch1",
        job=job,
        name="example-schedule",
        scope="sc1",
        code="cd1",
        expression="0 30 4 * * ? *",
        timezone="Europe/London",
        description="Example schedule",
        arguments={"username": username, "password": passwd},
    )

    return Deployment("configuration_example", [schedule, job, insItem, cs, username, passwd])

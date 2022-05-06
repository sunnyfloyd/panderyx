import factory

from panderyx.workflows.test.factories import WorkflowFactory


class ToolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tools.Tool"
        django_get_or_create = (
            "workflow",
            "name",
        )

    config = {"type": "input_url"}
    workflow = factory.SubFactory(WorkflowFactory)
    name = factory.Sequence(lambda n: f"tool{n}")

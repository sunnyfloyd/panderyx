import factory

from panderyx.users.test.factories import UserFactory


class WorkflowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "workflows.Workflow"
        django_get_or_create = (
            "user",
            "name",
        )

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"workflow{n}")

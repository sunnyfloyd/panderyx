import pytest
from django.forms.models import model_to_dict

from panderyx.workflows.serializers import WorkflowSerializer
from panderyx.workflows.test.factories import WorkflowFactory


@pytest.mark.django_db()
class TestWorkflowSerializer:
    @pytest.fixture()
    def setUp(self):
        self.workflow_data = model_to_dict(WorkflowFactory.build())

    def test_serializer_with_empty_data(self, setUp):
        serializer = WorkflowSerializer(data={})
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self, setUp):
        serializer = WorkflowSerializer(data=self.workflow_data)
        assert serializer.is_valid() is True

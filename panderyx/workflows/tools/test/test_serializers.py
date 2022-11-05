import pytest
from django.forms.models import model_to_dict
from rest_framework import exceptions

from panderyx.users.test.factories import UserFactory
from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.serializers.tool import ToolSerializer
from panderyx.workflows.tools.test.factories import ToolFactory


@pytest.mark.django_db()
class TestToolSerializer:
    @pytest.fixture()
    def setUp(self):
        self.user = UserFactory()
        self.workflow = WorkflowFactory(user=self.user)
        self.tool_1 = ToolFactory(workflow=self.workflow)
        self.tool_2 = ToolFactory(workflow=self.workflow)
        self.tool_3 = ToolFactory(workflow=self.workflow)

    def test_serializer_with_valid_data(self, setUp):
        serializer = ToolSerializer(data=model_to_dict(self.tool_1))
        assert serializer.is_valid() is True

    def test_serializer_with_empty_data(self, setUp):
        serializer = ToolSerializer(data={})
        assert serializer.is_valid() is False

    @pytest.mark.parametrize(
        "x,y,is_valid",
        [
            (-1, None, False),
            ("a", None, False),
            (None, -1, False),
            (None, "b", False),
        ],
    )
    def test_serializer_with_invalid_coordinates(self, setUp, x, y, is_valid):
        data = model_to_dict(self.tool_1)
        if x is not None:
            data["x"] = x
        if y is not None:
            data["y"] = y
        serializer = ToolSerializer(data=data)

        assert serializer.is_valid() is False

    def test_serializer_with_too_many_inputs(self, setUp):
        data = model_to_dict(self.tool_1)
        data["inputs"] = [self.tool_1.id, self.tool_2.id]
        serializer = ToolSerializer(data=data)

        with pytest.raises(exceptions.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)
            assert exc.value == "Number of inputs for this tool cannot be larger than 0"

    def test_serializer_with_invalid_type(self, setUp):
        data = model_to_dict(self.tool_1)
        data["config"] = {"type": "non_existing_type"}
        serializer = ToolSerializer(data=data)

        with pytest.raises(exceptions.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)
            assert exc.value == "Provided tool type does not exist."

    def test_serializer_with_non_json_config(self, setUp):
        data = model_to_dict(self.tool_1)
        data["config"] = "non_json_config"
        serializer = ToolSerializer(data=data)

        with pytest.raises(exceptions.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)
            assert exc.value == "Config must be in a JSON format."

    def test_serializer_without_type(self, setUp):
        data = model_to_dict(self.tool_1)
        data["config"] = {}
        serializer = ToolSerializer(data=data)

        with pytest.raises(exceptions.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)
            assert exc.value == "Config must include tool's type."

from django.forms.models import model_to_dict
from rest_framework import exceptions
from rest_framework.test import APITestCase

from panderyx.users.test.factories import UserFactory
from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.serializers.tool import ToolSerializer
from panderyx.workflows.tools.test.factories import ToolFactory


class TestToolSerializer(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.workflow = WorkflowFactory(user=self.user)
        self.tool_1 = ToolFactory(workflow=self.workflow)
        self.tool_2 = ToolFactory(workflow=self.workflow)
        self.tool_3 = ToolFactory(workflow=self.workflow)

    def test_serializer_with_valid_data(self):
        serializer = ToolSerializer(data=model_to_dict(self.tool_1))
        self.assertEqual(serializer.is_valid(), True)

    def test_serializer_with_empty_data(self):
        serializer = ToolSerializer(data={})
        self.assertEqual(serializer.is_valid(), False)

    # TODO This can be parametrized
    def test_serializer_with_invalid_coordinates(self):
        with self.subTest(msg="Invalid x coordinate"):
            data = model_to_dict(self.tool_1)
            data["x"] = -1
            serializer = ToolSerializer(data=data)
            self.assertEqual(serializer.is_valid(), False)

            data = model_to_dict(self.tool_1)
            data["x"] = "a"
            serializer = ToolSerializer(data=data)
            self.assertEqual(serializer.is_valid(), False)

        with self.subTest(msg="Invalid y coordinate"):
            data = model_to_dict(self.tool_1)
            data["y"] = -1
            serializer = ToolSerializer(data=data)
            self.assertEqual(serializer.is_valid(), False)

            data = model_to_dict(self.tool_1)
            data["y"] = "a"
            serializer = ToolSerializer(data=data)
            self.assertEqual(serializer.is_valid(), False)

        with self.subTest(msg="Invalid y coordinate"):
            data = model_to_dict(self.tool_1)
            data["y"] = -1
            serializer = ToolSerializer(data=data)
            self.assertEqual(serializer.is_valid(), False)

    def test_serializer_with_too_many_inputs(self):
        data = model_to_dict(self.tool_1)
        data["inputs"] = [self.tool_1.id, self.tool_2.id]
        serializer = ToolSerializer(data=data)

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "Number of inputs for this tool cannot be larger than 0",
        ):
            serializer.is_valid(raise_exception=True)

    def test_serializer_with_invalid_type(self):
        data = model_to_dict(self.tool_1)
        data["config"] = {"type": "non_existing_type"}
        serializer = ToolSerializer(data=data)

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "Provided tool type does not exist.",
        ):
            serializer.is_valid(raise_exception=True)

    def test_serializer_with_non_json_config(self):
        data = model_to_dict(self.tool_1)
        data["config"] = "non_json_config"
        serializer = ToolSerializer(data=data)

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "Config must be in a JSON format.",
        ):
            serializer.is_valid(raise_exception=True)

    def test_serializer_without_type(self):
        data = model_to_dict(self.tool_1)
        data["config"] = {}
        serializer = ToolSerializer(data=data)

        with self.assertRaisesMessage(
            exceptions.ValidationError,
            "Config must include tool's type.",
        ):
            serializer.is_valid(raise_exception=True)

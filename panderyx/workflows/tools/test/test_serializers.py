from datetime import datetime

from django.forms.models import model_to_dict
from django.test import TestCase

from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.serializers.tool import ToolSerializer
from panderyx.workflows.tools.test.factories import ToolFactory


class TestToolSerializer(TestCase):
    def setUp(self):
        self.workflow_data = model_to_dict(ToolFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = ToolSerializer(data={})
        assert serializer.is_valid() == False

    def test_serializer_with_invalid_data(self):
        with self.subTest(msg="Invalid x coordinate"):
            data = model_to_dict(ToolFactory.build())

            data["x"] = -1
            serializer = ToolSerializer(data=data)
            assert serializer.is_valid() == False

            data = model_to_dict(ToolFactory.build())

            data["x"] = "a"
            serializer = ToolSerializer(data=data)
            assert serializer.is_valid() == False

        with self.subTest(msg="Invalid y coordinate"):
            data = model_to_dict(ToolFactory.build())

            data["y"] = -1
            serializer = ToolSerializer(data=data)
            assert serializer.is_valid() == False

            data = model_to_dict(ToolFactory.build())

            data["y"] = "a"
            serializer = ToolSerializer(data=data)
            assert serializer.is_valid() == False

        with self.subTest(msg="Invalid y coordinate"):
            data = model_to_dict(ToolFactory.build())

            data["y"] = -1
            serializer = ToolSerializer(data=data)
            assert serializer.is_valid() == False

    def test_serializer_with_valid_data(self):
        serializer = ToolSerializer(data=self.workflow_data)
        assert serializer.is_valid() == True

import dataclasses
import json

from rest_framework import exceptions, serializers

from panderyx.workflows.models import Workflow
from panderyx.workflows.tools.dtos.input_tools import InputUrl
from panderyx.workflows.tools.models import Tool
from panderyx.workflows.tools.serializers.input_tools import InputUrlSerializer


class ConfigField(serializers.Field):
    def to_representation(self, value):
        if value["type"] == "input_url":
            config_serializer = InputUrlSerializer(data=value)
            config_serializer.is_valid()
            return config_serializer.data

    def to_internal_value(self, data):
        # data = data or "{}"
        # data_json = json.loads(data)
        # if self.parent.initial_data["type"] == "input_url":
        if data.get("type") == "input_url":
            dto = InputUrl(**data)
            return dataclasses.asdict(dto)
        return None

    def run_validation(self, data=serializers.empty):
        if not isinstance(data, dict):
            raise exceptions.ValidationError("Config must be in a JSON format.")
        if data.get("type") is None:
            raise exceptions.ValidationError("Config must include tool's type.")
        # except AttributeError:
        #     raise exceptions.ValidationError("Config data cannot be empty.")

        data = super().run_validation(data)

        # if data == serializers.empty:  # FIXME probably not needed since field is required
        #     raise exceptions.ValidationError("Config data must be provided.")
        # if not data:
        #     raise exceptions.ValidationError("Config data cannot be empty.")

        if data is None:
            raise exceptions.ValidationError("Provided tool type is invalid.")

        tool_type = data.get("type")
        if tool_type == "input_url":
            s = InputUrlSerializer(data=data)
            s.is_valid(raise_exception=True)

        return data


class ToolSerializer(serializers.ModelSerializer):
    config = ConfigField()

    class Meta:
        model = Tool
        fields = "__all__"
        read_only_fields = [
            "workflow",
            "data",
        ]

    def validate_inputs(self, value):
        if self.context:
            workflow_id = self.context["view"].kwargs["workflow_pk"]
            workflow = Workflow.objects.get(pk=workflow_id)

            for tool in value:
                if not workflow.tools.filter(pk=tool.id).exists():
                    raise exceptions.ValidationError(
                        "Provided input tool is not a part of this workflow."
                    )
        return value

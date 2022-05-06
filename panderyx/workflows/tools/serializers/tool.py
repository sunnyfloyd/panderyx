import dataclasses

from rest_framework import exceptions, serializers

from panderyx.workflows.models import Workflow
from panderyx.workflows.tools.dtos.input_tools import InputUrl
from panderyx.workflows.tools.helpers import ToolMapping
from panderyx.workflows.tools.models import Tool
from panderyx.workflows.tools.serializers.input_tools import InputUrlSerializer


class ConfigField(serializers.Field):
    def to_representation(self, value):
        serializer = ToolMapping[value["type"]].value["serializer"]
        config_serializer = serializer(data=value)
        config_serializer.is_valid()
        return config_serializer.data

    def to_internal_value(self, data):
        dto = ToolMapping[data.get("type")].value["dto"]
        config_dto = dto(**data)
        return dataclasses.asdict(config_dto)

    def run_validation(self, data=serializers.empty):
        if not isinstance(data, dict):
            raise exceptions.ValidationError("Config must be in a JSON format.")
        if data.get("type") is None:
            raise exceptions.ValidationError("Config must include tool's type.")

        data = super().run_validation(data)

        if data is None:
            raise exceptions.ValidationError("Provided tool type is invalid.")

        tool_type = data.get("type")
        serializer = ToolMapping[tool_type].value["serializer"]
        config_serializer = serializer(data=data)
        config_serializer.is_valid(raise_exception=True)

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

import dataclasses
import json

from rest_framework import exceptions, serializers

from panderyx.workflows.tools.dtos.input_tools import InputUrl
from panderyx.workflows.tools.models import Tool
from panderyx.workflows.tools.serializers.input_tools import InputUrlSerializer

# TODO
# tidy up below (check whether I can return DTO when calling
# to_internal_value) and whether I need DTOs at all in that case


class ConfigField(serializers.Field):
    def to_representation(self, value):
        if value["type"] == "input_url":
            s = InputUrlSerializer(data=value)
            s.is_valid()
            return s.data

    def to_internal_value(self, data):
        data_json = json.loads(data)
        if self.parent.initial_data["type"] == "input_url":
            dto = InputUrl(**data_json)
            return dataclasses.asdict(dto)

    def run_validation(self, data=...):
        data = super().run_validation(data)

        tool_type = self.parent.initial_data["type"]
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
        # TODO: Create validation to ensure that only tools from the current
        # workflow are accepted

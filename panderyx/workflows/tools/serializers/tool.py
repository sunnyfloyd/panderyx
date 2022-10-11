import dataclasses

from rest_framework import exceptions, serializers

from panderyx.workflows.models import Workflow
from panderyx.workflows.tools.mappings import ToolMapping
from panderyx.workflows.tools.models import Tool


class ConfigField(serializers.Field):
    def to_representation(self, value):
        serializer = ToolMapping[value["type"]].value["serializer"]
        config_serializer = serializer(data=value)
        config_serializer.is_valid()  # FIXME shouldn't I call validated_data instead of data after this?
        return config_serializer.data

    def to_internal_value(self, data):
        try:
            tool_mapping = ToolMapping[data.get("type")].value
        except KeyError:
            raise exceptions.ValidationError("Provided tool type does not exist.")

        dto = tool_mapping["dto"]
        max_number_of_inputs = tool_mapping["max_number_of_inputs"]
        data["max_number_of_inputs"] = max_number_of_inputs
        config_dto = dto(**data)
        return dataclasses.asdict(config_dto)

    def run_validation(self, data=serializers.empty):
        if not isinstance(data, dict):
            raise exceptions.ValidationError("Config must be in a JSON format.")
        if data.get("type") is None:
            raise exceptions.ValidationError("Config must include tool's type.")

        data = super().run_validation(data)

        # TODO Check whether below is needed (data should never be None here)
        # if data is None:
        #     raise exceptions.ValidationError("Provided tool type is invalid.")

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
            "max_number_of_inputs",
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

    def validate(self, data):
        # validate number of inputs
        max_number_of_inputs = data["config"]["max_number_of_inputs"]
        inputs = data.get("inputs")
        if inputs is not None and len(inputs) > max_number_of_inputs:
            raise exceptions.ValidationError(
                {
                    "config": f"Number of inputs for this tool cannot be larger than {max_number_of_inputs}"
                }
            )

        # validate uniqueness of tool name inside workflow
        workflow = self.context.get("workflow")
        if workflow and workflow.tools.filter(name=data["name"]).exists():
            raise exceptions.ValidationError(
                {"workflow": ["Tool's name must be unique in the workflow."]}
            )

        return data

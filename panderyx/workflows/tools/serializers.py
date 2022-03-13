from rest_framework import serializers

from panderyx.workflows.tools.models import Tool


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = "__all__"
        read_only_fields = [
            "workflow",
            "data",
        ]

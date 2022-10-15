from rest_framework import serializers

from panderyx.workflows.tools.serializers.tool_config import ToolConfigSerializer


class InputUrlConfigSerializer(ToolConfigSerializer):
    max_number_of_inputs = serializers.IntegerField(min_value=0, max_value=0, read_only=True)
    url = serializers.URLField(allow_blank=True)
    extension = serializers.CharField(allow_blank=True)
    separator = serializers.CharField(allow_blank=True)

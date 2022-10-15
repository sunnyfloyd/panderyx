from rest_framework import serializers

from panderyx.workflows.tools.serializers.tool_config import ToolConfigSerializer


class DescribeDataConfigSerializer(ToolConfigSerializer):
    max_number_of_inputs = serializers.IntegerField(min_value=1, max_value=1, read_only=True)
    data_type = serializers.IntegerField(min_value=0, max_value=3)

from rest_framework import serializers


class ToolConfigSerializer(serializers.Serializer):
    type = serializers.CharField()
    max_number_of_inputs = serializers.IntegerField(min_value=0, max_value=0, read_only=True)

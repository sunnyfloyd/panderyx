from rest_framework import serializers


class DescribeDataSerializer(serializers.Serializer):
    type = serializers.CharField()
    max_number_of_inputs = serializers.IntegerField(min_value=1, max_value=1, read_only=True)
    data_type = serializers.IntegerField(min_value=0, max_value=3)

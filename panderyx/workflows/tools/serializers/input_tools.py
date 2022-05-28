from rest_framework import serializers


class InputUrlSerializer(serializers.Serializer):
    type = serializers.CharField()
    max_number_of_inputs = serializers.IntegerField(min_value=0, max_value=0)
    url = serializers.URLField(allow_blank=True)
    extension = serializers.CharField(allow_blank=True)
    separator = serializers.CharField(allow_blank=True)

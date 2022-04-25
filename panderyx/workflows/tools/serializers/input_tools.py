from rest_framework import serializers


class InputUrlSerializer(serializers.Serializer):
    type = serializers.CharField()
    url = serializers.URLField()
    extension = serializers.CharField()

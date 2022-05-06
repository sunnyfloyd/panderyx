from rest_framework import serializers


class InputUrlSerializer(serializers.Serializer):
    type = serializers.CharField()
    url = serializers.URLField(allow_blank=True)
    extension = serializers.CharField(allow_blank=True)

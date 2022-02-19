from rest_framework import serializers

from panderyx.workflows.models import Workflow


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "date_created",
            "date_updated",
        ]

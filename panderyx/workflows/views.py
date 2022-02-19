from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from panderyx.workflows.models import Workflow
from panderyx.workflows.serializers import WorkflowSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from panderyx.common.permissions import IsWorkflowOwnerOrAdmin
from panderyx.tools.models import Tool
from panderyx.tools.serializers import ToolSerializer
from panderyx.workflows.models import Workflow


class ToolViewSet(viewsets.ModelViewSet):
    """ViewSet class for CRUD operations on Workflows."""

    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = (
        IsAuthenticated,
        IsWorkflowOwnerOrAdmin,
    )
    pagination_class = None

    def get_queryset(self):
        admin_permission = IsAdminUser()
        if admin_permission.has_permission(self.request, self):
            return Tool.objects.filter(workflow=self.kwargs["workflow_pk"])
        return Tool.objects.filter(
            Q(workflow=self.kwargs["workflow_pk"]) & Q(workflow__user=self.request.user)
        )

    def perform_create(self, serializer):
        workflow = get_object_or_404(Workflow, id=self.kwargs["workflow_pk"])
        serializer.save(workflow=workflow)

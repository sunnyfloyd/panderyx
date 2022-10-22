from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from panderyx.common.permissions import IsWorkflowOwnerOrAdmin
from panderyx.workflows.models import Workflow
from panderyx.workflows.serializers import WorkflowSerializer
from panderyx.workflows.services import WorkflowService


class WorkflowViewSet(viewsets.ModelViewSet):
    """ViewSet class for CRUD operations on Workflows."""

    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = (
        IsAuthenticated,
        IsWorkflowOwnerOrAdmin,
    )
    pagination_class = None

    def get_queryset(self):
        admin_permission = IsAdminUser()
        if admin_permission.has_permission(self.request, self):
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def run_workflow(self, request, pk=None):
        workflow = self.get_object()
        workflow_service = WorkflowService(workflow)
        workflow_service.run_workflow()
        data = workflow_service.get_outputs()

        return Response(data)

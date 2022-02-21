from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from panderyx.workflows.models import Workflow
from panderyx.workflows.permissions import IsObjectOwnerOrAdmin
from panderyx.workflows.serializers import WorkflowSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    """ViewSet class for CRUD operations on Workflows."""

    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = (
        IsAuthenticated,
        IsObjectOwnerOrAdmin,
    )
    pagination_class = None

    def get_queryset(self):
        admin_permission = IsAdminUser()
        if admin_permission.has_permission(self.request, self):
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

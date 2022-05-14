from rest_framework import permissions


class IsWorkflowOwnerOrAdmin(permissions.BasePermission):
    """
    Permission that allows only owners of an object or admins to view or edit it.

    This check is designed to work with both Workflow and Tool objects.
    """

    def has_object_permission(self, request, view, obj):
        # check for tool views
        if hasattr(obj, "workflow"):
            return obj.workflow.user == request.user or bool(
                request.user and request.user.is_staff
            )
        # check for workflow views
        else:
            return obj.user == request.user or bool(
                request.user and request.user.is_staff
            )

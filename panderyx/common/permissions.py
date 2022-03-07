from rest_framework import permissions


class IsWorkflowOwnerOrAdmin(permissions.BasePermission):
    """
    Permission that allows only owners of an object or admins to view or edit it.
    It takes into account
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "workflow"):
            return obj.workflow.user == request.user or bool(
                request.user and request.user.is_staff
            )
        else:
            return obj.user == request.user or bool(
                request.user and request.user.is_staff
            )

from rest_framework import permissions


class IsObjectOwnerOrAdmin(permissions.BasePermission):
    """
    Permission that allows only owners of an object or admins to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or bool(request.user and request.user.is_staff)

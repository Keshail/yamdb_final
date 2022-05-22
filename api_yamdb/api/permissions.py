from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Custom permission to only allow admins to read or edit."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthorModeratorAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка наличие прав админа. Если нет - то только чтение."""

    def has_permission(self, request, view):
        return (request.user.role == "admin" or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin" or request.user.is_staff

class Smth(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (request.user.role == "admin" or request.user.is_staff)
        return True

    def has_object_permission(self, request, view, obj):
        return True

class IsAuthorOrAdmin(permissions.BasePermission):
    """Проверка авторства. Если нет - то только чтение."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (obj.author == request.user or request.user.role == "admin" or request.user.is_staff)
        )

class IsModeratorOrReadOnly(permissions.BasePermission):
    """Проверка наличие прав админа. Если нет - то только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.role == "moderator"
        )


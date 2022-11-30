from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка наличие прав админа. Если нет - то только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.role == "admin"
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверка авторства. Если нет - то только чтение."""

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated and obj.author == request.user
        return True

class IsModeratorOrReadOnly(permissions.BasePermission):
    """Проверка наличие прав админа. Если нет - то только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.role == "moderator"
        )


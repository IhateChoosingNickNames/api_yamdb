from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка наличие прав админа."""

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка наличие прав админа. Если нет - только чтение."""

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_staff
                or request.user.is_superuser
            )
        return True

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_staff
                or request.user.is_superuser
            )
        return True


class IsAdminOrModOrReadOnly(permissions.BasePermission):
    """Проверка на админа или модератора. Если нет - только чтение."""

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user.is_staff
                or request.user.is_superuser
                or request.user.id == obj.author.id
            )
        return True


class IsAuthorOrAdmin(permissions.BasePermission):
    """Проверка авторства."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj.author == request.user
            or request.user.is_admin
            or request.user.is_staff
            or request.user.is_superuser
        )

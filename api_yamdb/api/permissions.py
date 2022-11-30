from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """ Пермишен доступа к API запрашиваемый медом является безопасным
     или доступен только для администратора."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )

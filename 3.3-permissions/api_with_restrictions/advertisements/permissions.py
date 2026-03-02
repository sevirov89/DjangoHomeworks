from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """Разрешение на изменение/удаление только для владельца или администратора."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user.is_staff
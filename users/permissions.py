from rest_framework import permissions


class IsUserProfile(permissions.BasePermission):
    """ Проверка является ли профиль данного пользователя."""

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id:
            return True
        return False
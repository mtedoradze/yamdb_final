from rest_framework import permissions

from users.models import User


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.USER
            and request.method in permissions.SAFE_METHODS
            or obj.id == request.user.id
            or request.user.is_staff
        )


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_anonymous:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if obj.author == request.user:
                return True

            if request.user.role == User.ADMIN:
                return True

            if request.user.role == User.MODERATOR:
                return True

        return False


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or request.user.is_authenticated
            and request.user.role == User.ADMIN
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated and request.user.role == User.ADMIN
        ):
            return True

        return any([
            request.user.is_staff,
            request.method in permissions.SAFE_METHODS,
        ])

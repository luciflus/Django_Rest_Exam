from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and obj.author == request.user.author
        )

class IsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj): ##update, delete
        return bool(request.user and request.user.is_staff)
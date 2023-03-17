from rest_framework import permissions
from src.constants import ROLE_SUPERADMIN

class IsSuperAdmin(permissions.BasePermission):
    message = "Must have Super Admin role"

    def has_permission(self, request, view):
        if ROLE_SUPERADMIN in request.user.get('roles'):
            return True

        return False
    
    def has_object_permission(self, request, view, obj):
        if ROLE_SUPERADMIN in request.user.get('roles'):
            return True

        return False
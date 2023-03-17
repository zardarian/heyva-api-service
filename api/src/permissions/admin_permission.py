from rest_framework import permissions
from src.constants import ROLE_SUPERADMIN, ROLE_ADMIN

class IsAdmin(permissions.BasePermission):
    message = "Must have Admin role"

    def has_permission(self, request, view):
        if (ROLE_SUPERADMIN in request.user.get('roles')) or (ROLE_ADMIN in request.user.get('roles')):
            return True

        return False
    
    def has_object_permission(self, request, view, obj):
        if (ROLE_SUPERADMIN in request.user.get('roles')) or (ROLE_ADMIN in request.user.get('roles')):
            return True

        return False
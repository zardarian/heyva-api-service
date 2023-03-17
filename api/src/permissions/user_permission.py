from rest_framework import permissions
from src.constants import ROLE_SUPERADMIN, ROLE_ADMIN, ROLE_USER

class IsUser(permissions.BasePermission):
    message = "Must have User role"

    def has_permission(self, request, view):
        if (ROLE_SUPERADMIN in request.user.get('roles')) or (ROLE_ADMIN in request.user.get('roles')) or (ROLE_USER in request.user.get('roles')):
            return True

        return False
    
    def has_object_permission(self, request, view, obj):
        if (ROLE_SUPERADMIN in request.user.get('roles')) or (ROLE_ADMIN in request.user.get('roles')) or (ROLE_USER in request.user.get('roles')):
            return True

        return False
from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow usser to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Checks user is trying to edit their own profle"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id
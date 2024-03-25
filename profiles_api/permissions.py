from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow usser to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Checks user is trying to edit their own profle"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id
    

class UpdateOwnStatus(permissions.BasePermission):
    """Allows users to update their one status"""

    def has_object_permission(self, request, view, obj):
        """Checks the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id == request.user.id
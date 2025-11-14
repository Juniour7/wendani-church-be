from rest_framework.permissions import BasePermission

class IsTreasurer(BasePermission):
    """
    Allows access only to users with role 'treasurer'.
    """

    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and getattr(request.user, "role", None) == "treasurer"
        )

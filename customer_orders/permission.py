from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission class that grants access only to the owners of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the authenticated user is the owner of the object.

        Args:
            request: The request object.
            view: The view that is being accessed.
            obj: The object being checked for permissions.

        Returns:
            bool: True if the user is the owner, False otherwise.
        """
        return obj.user == request.user

import logging
from rest_framework import permissions

logger = logging.getLogger('customer_orders')  

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
        is_owner = obj.user == request.user
        if is_owner:
            logger.info('Access granted to user: %s for object: %s', request.user, obj)
        else:
            logger.warning('Access denied to user: %s for object: %s', request.user, obj)

        return is_owner
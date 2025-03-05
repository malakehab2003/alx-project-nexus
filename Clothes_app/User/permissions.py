from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from .utils.authentication import get_user_from_request
from .models import Address

User = get_user_model()

class IsOwnerOrForbidden(BasePermission):
    """Allow users to modify only their own data"""
    def has_permission(self, request, view):
        """Ensure the request is authenticated"""
        user = get_user_from_request(request)
        if not user:
            return False
        request.user = user
        return True

    def has_object_permission(self, request, view, obj):
        """Ensure the user is modifying their own data"""
        if isinstance(obj, User):
            return obj.id == request.user["id"]

isOwnerOrForbidden = IsOwnerOrForbidden()
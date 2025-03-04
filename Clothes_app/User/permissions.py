from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .utils.redis import Redis
from .serialzers import UserSerializer
import json

User = get_user_model()

class IsOwnerOrForbidden(BasePermission):
    """Allow users to modify only their own data"""

    def remove_prefix_from_header_return_token(self, header):
        """Remove the prefix from the token"""
        if not header or not header.startswith("Bearer "):
            return None
        return header.split(" ")[1]

    def get_validated_token_from_request(self, request):
        """Get the validated token from the request"""
        auth = JWTAuthentication()
        header = request.headers.get("Authorization")
        token = self.remove_prefix_from_header_return_token(header)

        if not token:
            return None

        try:
            return auth.get_validated_token(token)
        except Exception:
            return None

    def has_permission(self, request, view):
        """Ensure the request is authenticated"""
        validated_token = self.get_validated_token_from_request(request)

        if not validated_token:
            return False

        user_id = validated_token.get("user_id")

        if not user_id:
            return False

        user = Redis.get_data_from_redis(validated_token)

        if not user:
            try:
                user = User.objects.get(id=user_id)
                user_data = UserSerializer(user).data
                Redis.save_data_in_redis(validated_token, user=user_data)
            except User.DoesNotExist:
                return False

        request.user = user
        return True

    def has_object_permission(self, request, view, obj):
        """Ensure the user is modifying their own data"""
        if isinstance(request.user, dict):
            return obj.id == request.user["user"]["id"]
        return obj.id == request.user.id

isOwnerOrForbidden = IsOwnerOrForbidden()
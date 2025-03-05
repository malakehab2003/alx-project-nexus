from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from ..utils.redis import Redis
from ..serialzers import UserSerializer


User = get_user_model()

def remove_prefix_from_header_return_token(header):
    """Remove the prefix from the token"""
    if not header or not header.startswith("Bearer "):
        return None
    return header.split(" ")[1]

def get_validated_token_from_request(request):
    """Get the validated token from the request"""
    auth = JWTAuthentication()
    header = request.headers.get("Authorization")
    token = remove_prefix_from_header_return_token(header)

    if not token:
        return None

    try:
        return auth.get_validated_token(token)
    except Exception:
        return None
    
def get_user_from_request(request):
    """ get user from request """
    validated_token = get_validated_token_from_request(request)

    if not validated_token:
        return None
    
    user_id = validated_token.get("user_id")

    if not user_id:
        return None
    
    user_data = Redis.get_data_from_redis(validated_token)

    if not user_data:
        try:
            user = User.objects.get(id=user_id)
            user_data = UserSerializer(user).data
            Redis.save_data_in_redis(validated_token, user=user_data)
        except User.DoesNotExist:
            return None
    else:
        user_data = user_data["user"]
    return user_data
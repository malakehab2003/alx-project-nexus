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

def validate_token(token):
    """ take token and validate it """
    auth = JWTAuthentication()
    try:
        return auth.get_validated_token(token)
    except Exception:
        return None

def get_validated_token_from_request(request):
    """Get the validated token from the request"""
    header = request.headers.get("Authorization")
    token = remove_prefix_from_header_return_token(header)

    if not token:
        return None

    return validate_token(token)
    
def get_user_id_from_token(token):
    """ get the id of the user from the jwt token """
    user_id = token.get("user_id")
    return user_id
    
def get_user_from_request(request):
    """ get user from request """
    validated_token = get_validated_token_from_request(request)

    if not validated_token:
        return None
    
    user_id = get_user_id_from_token(validated_token)

    if not user_id:
        return None
    
    user_data = Redis.get_data_from_redis(user_id)

    if not user_data:
        try:
            user = User.objects.get(id=user_id)
            user_data = UserSerializer(user).data
            Redis.save_data_in_redis(user_id, user=user_data)
        except User.DoesNotExist:
            return None
    else:
        user_data = user_data["user"]
    return user_data
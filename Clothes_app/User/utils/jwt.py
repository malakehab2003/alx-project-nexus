from rest_framework_simplejwt.tokens import RefreshToken
from .redis import Redis

class JWT:
    """Class to handle JWT tokens"""
    @staticmethod
    def create_token(user):
        """Create a token for the user"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return access_token, refresh_token
    
    @staticmethod
    def get_new_access_token(refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return new_access_token
        except Exception as e:
            return str(e)
        
    @staticmethod
    def blacklist_refresh_token(refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return True
        except Exception as e:
            return str(e)

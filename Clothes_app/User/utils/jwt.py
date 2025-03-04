from rest_framework_simplejwt.tokens import RefreshToken

class JWT:
    """Class to handle JWT tokens"""
    @staticmethod
    def create_token(user):
        """Create a token for the user"""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return access_token

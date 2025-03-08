from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..utils.validate import validate_email, validate_password, validate_args_not_none
from ..utils.jwt import JWT
from ..utils.redis import Redis
from ..models import User
from ..serialzers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from ..utils.create_verification import create_verification_and_send_email
from ..permissions import isOwnerOrForbidden
from ..utils.authentication import get_user_from_request, validate_token, get_user_id_from_token, get_token_from_request
from django.shortcuts import get_object_or_404
from Shop.models import Cart


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for the User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    no_auth_actions = [
            "create",
            "validate_email",
            "signin",
            "resend_verification",
            "forget_password",
            "reset_password",
            "list"
        ]

    def get_permissions(self):
        """Allow public access for create, require authentication for others"""
        if self.action in self.no_auth_actions:
            return []
        return [IsAuthenticated(), isOwnerOrForbidden]
    
    @action(detail=False, methods=["post"], url_path="validate_email")
    def validate_email(self, request):
        """validate the email of the user"""
        email = request.data.get("email")
        name = request.data.get("name")
        password = request.data.get("password")

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_args_not_none(name)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        verification_code = create_verification_and_send_email(email)
        Redis.save_data_in_redis(email, name=name, password=password, verification_code=verification_code)

        return Response({"message": "Email sent for verification"}, status=status.HTTP_200_OK)

    
    def create(self, request):
        """Create a user"""
        # get data from request
        verrification_code = request.data.get("verification_code")
        email = request.data.get("email")

        # check data
        restricted_fields = [
            "is_staff",
            "is_superuser",
            "is_active",
            "is_deleted",
            "is_verified"
        ]

        for field in restricted_fields:
            if field in request.data:
                return Response(
                    {"error": f"You are not allowed to add {field}."},
                    status=status.HTTP_403_FORBIDDEN
                )

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Redis.check_data_in_redis(email):
            return Response({"error": "Data not found in Redis"}, status=status.HTTP_400_BAD_REQUEST)
        
        # get saved data
        user_data = Redis.get_data_from_redis(email)
        if user_data["verification_code"] != verrification_code:
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

        # remove verification_code and add verified
        del user_data["verification_code"]
        user_data["is_verified"] = True

        # create user object and remove cached data
        user = User.objects.create_user(email=email, **user_data)
        Redis.delete_data_from_redis(email)

        # serialize data
        data = UserSerializer(user).data

        # create user cart
        Cart.objects.create(
            user = user
        )

        # create token and validate and save user data in cache
        access_token, refresh_token = JWT.create_token(user)
        validated_token = validate_token(access_token)
        user_id = get_user_id_from_token(validated_token)
        Redis.save_data_in_redis(user_id, user=data, timeout=604800)

        return Response({"access_token": access_token, "refresh_token": refresh_token, "user": data}, status=status.HTTP_201_CREATED)

    
    @action(detail=False, methods=["post"], url_path="signin")
    def signin(self, request):
        """Login a user"""
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        access_token, refresh_token = JWT.create_token(user)

        user_data = UserSerializer(user).data
        user_id = user_data["id"]

        user.is_active = True
        user.save()

        if not Redis.check_data_in_redis(user_id):
            Redis.save_data_in_redis(user_id, user=user_data, timeout=604800)


        return Response({"access_token": access_token, "refresh_token": refresh_token, "user": user_data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path="resend_verification")
    def resend_verification(self, request):
        """Resend the verification email"""
        email = request.data.get("email")

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        verification_code = create_verification_and_send_email(email)

        if Redis.check_data_in_redis(email):
            user_data = Redis.get_data_from_redis(email)
            user_data["verification_code"] = verification_code
            Redis.save_data_in_redis(email, **user_data, timeout=600)
        else:
            return Response({"message": "Create new user"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Email sent for verification"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path="forget_password")
    def forget_password(self, request):
        """Forget password"""
        email = request.data.get("email")

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        verification_code = create_verification_and_send_email(email)

        Redis.save_data_in_redis(email, verification_code=verification_code, timeout=600)

        return Response({"message": "Email sent for verification"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path="reset_password")
    def reset_password(self, request):
        """Reset the password"""
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")
        password = request.data.get("password")

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        user_data = Redis.get_data_from_redis(email)
        if user_data["verification_code"] != verification_code:
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        Redis.delete_data_from_redis(email)

        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """ update user """
        restricted_fields = [
            "is_staff",
            "is_superuser",
            "password",
            "is_active",
            "is_deleted",
            "is_verified",
            "email",
        ]

        id_from_url_params = kwargs.get("pk")
        user_id_from_token = get_user_from_request(request).get("id")


        for field in restricted_fields:
            if field in request.data:
                return Response(
                    {"error": f"You are not allowed to update {field}."},
                    status=status.HTTP_403_FORBIDDEN
                )

        try:
            validate_args_not_none(id_from_url_params, user_id_from_token)
            id_from_url_params = int(id_from_url_params)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        if user_id_from_token != id_from_url_params:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().update(request, *args, **kwargs, partial=True)
    
    @action(detail=False, methods=["post"], url_path="signout")
    def signout(self, request, *args, **kwargs):
        """ sign out the user and expire his access token and blacklist his refresh token """
        refresh_token = request.data.get("refresh_token")
        access_token = get_token_from_request(request)
        valdated_token = validate_token(access_token)
        user_id = get_user_id_from_token(valdated_token)

        user = get_object_or_404(User, id=user_id)

        if not refresh_token:
            return Response({"error": "refresh token is requried"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            JWT.blacklist_refresh_token(str(refresh_token))
            user.is_active = False
            user.save()
            Redis.delete_data_from_redis(user.id)
            return Response({"message": "sign out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="refresh_token")
    def refresh_token(self, request, *args, **kwargs):
        """ refresh the access token """
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "refresh token is requried"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_token = JWT.get_new_access_token(refresh_token)
            return Response({"access_token": new_token}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "can't refresh token"}, status=status.HTTP_400_BAD_REQUEST)



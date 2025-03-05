from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..utils.validate import validate_email, validate_password, validate_args_not_none
from ..utils.jwt import JWT
from ..utils.redis import Redis
from ..models import User, Address, PromoCode, Notification, Payment
from ..serialzers import UserSerializer, AddressSerializer, PromoCodeSerializer, NotificationSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from ..utils.create_verification import create_verification_and_send_email
from ..permissions import isOwnerOrForbidden
from ..utils.authentication import get_user_from_request
from ..utils.authentication import get_user_id_from_token

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
        verrification_code = request.data.get("verification_code")
        email = request.data.get("email")

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Redis.check_data_in_redis(email):
            return Response({"error": "Data not found in Redis"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_data = Redis.get_data_from_redis(email)
        if user_data["verification_code"] != verrification_code:
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

        del user_data["verification_code"]
        user_data["is_verified"] = True

        user = User.objects.create_user(email=email, **user_data)
        Redis.delete_data_from_redis(email)

        data = UserSerializer(user).data

        access_token = JWT.create_token(user)
        user_id = get_user_id_from_token(access_token)
        Redis.save_data_in_redis(user_id, user=data, timeout=604800)

        user_data = UserSerializer(user).data
        return Response({"access_token": access_token, "user": user_data}, status=status.HTTP_201_CREATED)
    

    
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

        access_token = JWT.create_token(user)

        user_data = UserSerializer(user).data
        user_id = user_data["id"]

        if not Redis.check_data_in_redis(user_id):
            Redis.save_data_in_redis(user_id, user=user_data, timeout=604800)


        return Response({"access_token": access_token, "user": user_data}, status=status.HTTP_200_OK)
    
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
        password = request.data.get("password")
        email = request.data.get("email")
        id = kwargs.get("pk")
        user = get_user_from_request(request)

        try:
            validate_args_not_none(id, user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not id:
            return Response({"error": "id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        if user["email"] != email:
            return Response({"error": "Email can't be updated"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().update(request, *args, **kwargs)



class PromoCodeViewSet(viewsets.ModelViewSet):
    """ViewSet for the PromoCode model."""
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [IsAuthenticated]


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Notification model."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Payment model."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

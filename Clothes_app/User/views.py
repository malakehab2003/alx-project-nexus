from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Address, PromoCode, Notification, Payment
from .serialzers import UserSerializer, AddressSerializer, PromoCodeSerializer, NotificationSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

def create_token(user):
    """Create a token for the user"""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return access_token

def validate_serializer(serializer):
    """Validate the serializer"""
    serializer.is_valid(raise_exception=True)
    return serializer

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for the User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        """Allow public access for create, require authentication for others"""
        if self.action == "create":
            return []
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Create a user"""
        serializer = self.get_serializer(data=request.data)
        serializer = validate_serializer(serializer)
        user = User.objects.create_user(**serializer.validated_data)
        access_token = create_token(user)
        return Response({"access_token": access_token, "user": user}, status=status.HTTP_201_CREATED)


class AddressViewSet(viewsets.ModelViewSet):
    """ViewSet for the Address model."""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


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

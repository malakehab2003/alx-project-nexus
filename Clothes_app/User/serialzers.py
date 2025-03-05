from rest_framework import serializers
from .models import User, Address, PromoCode, Notification, Payment

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True},
            'is_deleted': {'read_only': True},
            'is_staff': {'read_only': True},
        }

class AddressSerializer(serializers.ModelSerializer):
    """Serializer for the Address model."""
    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {"user":{"read_only":True}}

class PromoCodeSerializer(serializers.ModelSerializer):
    """Serializer for the PromoCode model."""
    class Meta:
        model = PromoCode
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for the Notification model."""
    class Meta:
        model = Notification
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for the Payment model."""
    class Meta:
        model = Payment
        fields = '__all__'

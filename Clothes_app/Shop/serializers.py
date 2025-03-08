from rest_framework import serializers
from .models import Cart, Wishlist, Orders, OrderItem, CartItems

class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemsSerializer(serializers.ModelSerializer):
    """Serializer for the cart items model."""
    class Meta:
        model= CartItems
        fields= '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for the Wishlist model."""
    class Meta:
        model = Wishlist
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    """Serializer for the Orders model."""
    class Meta:
        model = Orders
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the OrderItem model."""
    class Meta:
        model = OrderItem
        fields = '__all__'
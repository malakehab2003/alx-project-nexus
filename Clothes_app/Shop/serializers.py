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
    address = serializers.StringRelatedField()
    
    class Meta:
        model = Orders
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the OrderItem model."""
    color_name = serializers.SerializerMethodField()
    size_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_color_name(self, obj):
        return obj.color.name if obj.color else None

    def get_size_name(self, obj):
        return obj.size.name if obj.size else None
    
    def get_product_name(self, obj):
        return obj.product.name if obj.product else None
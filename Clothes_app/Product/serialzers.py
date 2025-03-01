from rest_framework import serializers
from .models import Product, Category, Image, Review, Brand, Size, Color

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    class Meta:
        model = Category
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    """Serializer for the Image model."""
    class Meta:
        model = Image
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""
    class Meta:
        model = Review
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    """Serializer for the Brand model."""
    class Meta:
        model = Brand
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    """Serializer for the Size model."""
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    """Serializer for the Color model."""
    class Meta:
        model = Color
        fields = '__all__'

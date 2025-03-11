from rest_framework import serializers
from .models import Product, Category, Image, Review, Brand, Size, Color

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""
    brands_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_brands_name(self, obj):
        return [brand.name for brand in obj.brands.all()]

    def get_category_name(self, obj):
        return [category.name for category in obj.category.all()]

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

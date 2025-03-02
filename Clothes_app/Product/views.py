from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, Brand, Image, Review, Size, Color
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, ImageSerializer, ReviewSerializer, SizeSerializer, ColorSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for the Product model."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Category model."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class BrandViewSet(viewsets.ModelViewSet):
    """ViewSet for the Brand model."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]

class ImageViewSet(viewsets.ModelViewSet):  
    """ViewSet for the Image model."""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for the Review model."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class SizeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Size model."""
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated]

class ColorViewSet(viewsets.ModelViewSet):
    """ViewSet for the Color model."""
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAuthenticated]

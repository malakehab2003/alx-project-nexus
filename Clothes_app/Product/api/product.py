from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from ..models import Product, Size, Color
from ..serialzers import ProductSerializer, SizeSerializer, ColorSerializer

class ProductViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """ViewSet for the Product model."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
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

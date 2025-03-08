from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from ..models import Product
from ..serialzers import ProductSerializer

class ProductViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """ViewSet for the Product model."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

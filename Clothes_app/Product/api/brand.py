from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Brand, Product
from ..serialzers import BrandSerializer, ProductSerializer


class BrandViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """ViewSet for the Brand model."""
    queryset = Brand.objects.all()
    lookup_field = "pk"
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        brand_id = kwargs.get("pk")

        if not brand_id:
            return Response({"error": "required id"}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(brands=brand_id)
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)

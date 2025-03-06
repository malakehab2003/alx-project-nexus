from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Category, Product
from ..serialzers import CategorySerializer, ProductSerializer


class CategoryViewSet(mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """ViewSet for the Category model."""
    queryset = Category.objects.all()
    lookup_field = "pk"
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        category_id = kwargs.get("pk")

        if not category_id:
            return Response({"error": "required id"}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(category=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)
        

# signout
# return products with brand, category

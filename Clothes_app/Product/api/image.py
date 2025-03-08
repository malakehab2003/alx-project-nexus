from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from User.utils.authentication import get_user_from_request
from ..serialzers import ImageSerializer
from ..models import Image, Product


class ImageViewSet(viewsets.GenericViewSet):  
    """ViewSet for the Image model."""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["get"], url_path='get_product_photos/(?P<product_id>[^/.]+)')
    def get_product_photos(self, request, product_id=None):
        """ get photos of a product """
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "No authorization"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        images = Image.objects.filter(product=product)
        serializer = ImageSerializer(images, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


        

from ..models import Color, Product
from ..serialzers import ColorSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from User.utils.authentication import get_user_from_request


class ColorViewSet(viewsets.GenericViewSet):
    """ViewSet for the Color model."""
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path='get_product_colors/(?P<product_id>[^/.]+)')
    def get_product_colors(self, request, product_id=None):
        """ get all colors of a product """
        product = get_object_or_404(Product, id=product_id)
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "No authorization"}, status=status.HTTP_401_UNAUTHORIZED)

        colors = Color.objects.filter(product=product_id)
        serializer = ColorSerializer(colors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




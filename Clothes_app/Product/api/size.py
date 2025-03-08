from ..models import Size, Product
from ..serialzers import SizeSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from User.utils.authentication import get_user_from_request


class SizeViewSet(viewsets.GenericViewSet):
    """ViewSet for the Size model."""
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path='get_product_sizes/(?P<product_id>[^/.]+)')
    def get_product_sizes(self, request, product_id=None):
        """ get all sizes of a product """
        product = get_object_or_404(Product, id=product_id)
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "No authorization"}, status=status.HTTP_401_UNAUTHORIZED)

        sizes = Size.objects.filter(product=product_id)
        serializer = SizeSerializer(sizes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




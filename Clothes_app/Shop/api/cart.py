from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Cart, CartItems
from Product.models import Product, Color, Size
from ..serializers import CartSerializer, CartItemsSerializer
from User.utils.authentication import get_user_from_request
from django.shortcuts import get_object_or_404



class CartViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet for the Cart model."""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """ list all products user added to cart """
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "not autorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        cart = get_object_or_404(Cart, user=user_id)


        items = CartItems.objects.filter(cart=cart.id)

        items_data = []
        for item in items:
            items_data.append({
                "product_name": item.product.name,
                "product_id": item.product.id,
                "color": item.color.name if item.color else None,
                "size": item.size.name if item.size else None,
                "quantity": item.quantity,
            })

        return Response({"items": items_data}, status=status.HTTP_200_OK)

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import  Wishlist
from Product.models import Product
from Product.serialzers import ProductSerializer
from User.models import User
from ..serializers import WishlistSerializer
from User.utils.authentication import get_user_from_request
from django.shortcuts import get_object_or_404


class WishlistViewSet(viewsets.GenericViewSet):
    """ViewSet for the Wishlist model."""
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="add_to_withlist")
    def add_to_withlist(self, request, *args, **kwargs):
        """ add item to the user wishlist """
        user_id = get_user_from_request(request).get("id")
        product_id = request.data.get("product")

        if not user_id:
            return Response({"error": "not autorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not product_id:
            return Response({"error": "product id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, id=user_id)

        Wishlist.objects.create(
            product=product,
            user=user,
        )

        return Response({"message": "product added to the wishlist correctly"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"],url_path="remove_product")
    def remove_product(self, request, *args, **kwargs):
        """ Remove item from the wishlist """
        user_id = get_user_from_request(request).get("id")
        product_id = request.data.get("product")

        if not user_id:
            return Response({"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        wishlist_item = Wishlist.objects.filter(user=user_id, product=product_id)
        if not wishlist_item.exists():
            return Response({"error": "Product not found in wishlist"}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item.delete()
        
        return Response({"message": "Product removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=["get"], url_path="get_user_wishlist")
    def get_user_wishlist(self, request, *args, **kwargs):
        """ get wishlist products of user """
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        wishlist_items = Wishlist.objects.filter(user=user_id)
        
        products = [wishlist_item.product for wishlist_item in wishlist_items]

        serialized_products = ProductSerializer(products, many=True).data

        return Response(serialized_products, status=status.HTTP_200_OK)


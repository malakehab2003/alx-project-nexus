from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import CartItems, Cart
from ..serializers import CartItemsSerializer
from Product.models import Product, Size, Color
from User.utils.authentication import get_user_from_request
from django.shortcuts import get_object_or_404


class CartItemsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """ViewSet for the Cart items model."""
    queryset = CartItems.objects.all()
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]

    def check_validated_data(self, product, size_id, color_id, quantity):
        """ check if user can add this data to the cart 
            check if the product have stock
            check if size is available
            check if color is available
        """
        if product.stock < quantity:
            return "cannot add this quantity"
        
        if not Size.objects.filter(id=size_id, product=product).exists():
            return "Selected size is not available"
        
        if not Color.objects.filter(id=color_id, product=product).exists():
            return "Selected color is not available"
        
        return None
        

    def create(self, request, *args, **kwargs):
        """ create a new cart item """
        user_id = get_user_from_request(request).get("id")
        product_id = request.data.get("product")
        color_id = request.data.get("color")
        size_id = request.data.get("size")
        quantity = request.data.get("quantity")
        
        if not user_id:
            return Response({"error": "not autorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not product_id:
            return Response({"error": "product id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, user=user_id)
        size = get_object_or_404(Size, id=size_id)
        color = get_object_or_404(Color, id=color_id)

        validate_data = self.check_validated_data(product, size_id, color_id, quantity)     

        if validate_data:
            return Response({"error": validate_data}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = CartItems.objects.create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            quantity=quantity
        )

        cart.total_price += (product.price * quantity)
        cart.save()

        
        cart_item_data = {
            "id": cart_item.id,
            "cart": cart.id,
            "product": product.id,
            "size": size.name,
            "color": color.name,
            "quantity": quantity
        }

        return Response(cart_item_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """ update order item """
        user_id = get_user_from_request(request).get("id")
        quantity = request.data.get("quantity")
        cart_item_id = kwargs.get("pk")

        if not user_id:
            return Response({"error": "not autorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        cart = get_object_or_404(Cart, user=user_id)
        cart_item = get_object_or_404(CartItems, id=cart_item_id)

        cart.total_price -= cart_item.product.price * cart_item.quantity
        cart.total_price += cart_item.product.price * quantity

        cart.save()

        request.data["cart"] = cart.id

        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """ remove item from the cart item """
        cart_item_id = kwargs.get("pk")

        if not cart_item_id:
            return Response({"error": "cart item id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = get_object_or_404(CartItems, id=cart_item_id)
        cart = get_object_or_404(Cart, id=cart_item.cart.id)

        cart.total_price -= cart_item.product.price * cart_item.quantity
        cart.save()

        return super().destroy(request, *args, **kwargs)

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, Orders, OrderItem, Wishlist
from .serializers import CartSerializer, OrdersSerializer, OrderItemSerializer, WishlistSerializer

class CartViewSet(viewsets.ModelViewSet):
    """ViewSet for the Cart model."""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class OrdersViewSet(viewsets.ModelViewSet):
    """ViewSet for the Orders model."""
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

class OrderItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem model."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

class WishlistViewSet(viewsets.ModelViewSet):
    """ViewSet for the Wishlist model."""
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]


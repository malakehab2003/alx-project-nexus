from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Orders, OrderItem
from .serializers import OrdersSerializer, OrderItemSerializer

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


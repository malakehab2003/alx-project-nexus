from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import OrderItem, Orders
from ..serializers import OrderItemSerializer
from django.shortcuts import get_object_or_404
from User.utils.authentication import get_user_from_request
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderItemViewSet(viewsets.GenericViewSet):
    """ViewSet for the OrderItem model."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "order_id"

    @action(detail=False, methods=['get'], url_path='by-order/(?P<order_id>\d+)')
    def list_by_order(self, request, order_id=None):
        """ Custom action to list order items for a specific order """
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "not authorized"}, status=401)

        order = get_object_or_404(Orders, id=order_id, user=user_id)
        order_items = OrderItem.objects.filter(order=order)
        
        serializer = self.get_serializer(order_items, many=True)
        return Response(serializer.data)


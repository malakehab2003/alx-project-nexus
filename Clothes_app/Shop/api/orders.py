from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Orders, OrderItem, CartItems, Cart
from User.models import Notification, User
from ..serializers import OrdersSerializer
from User.utils.authentication import get_user_from_request
from django.shortcuts import get_object_or_404
import datetime


class OrdersViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet,

    ):
    """ViewSet for the Orders model."""
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def create_notification(self, user_id, message, description):
        """ send notifcation after creating a new order """
        user = get_object_or_404(User, id=user_id)

        Notification.objects.create(
            user=user,
            message=message,
            description=description
        )

    def comvert_cart_items_to_order_items(self, user_id, order_id):
        """ get all the cart items of the user and make them order items """
        cart = Cart.objects.get(user=user_id)

        order = Orders.objects.get(id=order_id)
        order.total_price = cart.total_price
        order.save()

        cart_items = CartItems.objects.filter(cart=cart.id)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                color=item.color,
                size=item.size,
            )
            cart_items.delete()

    def list(self, request, *args, **kwargs):
        """ list all orders of user """
        user_id = get_user_from_request(request).get("id")
        status = request.query_params.get("status")

        if not user_id:
            return Response({"error": "not autorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if status not in ["active", "cancelled", "completed"]:
            return Response({"error": "wrong status"}, status=status.HTTP_400_BAD_REQUEST)
        
        orders = Orders.objects.filter(user=user_id, status=status)

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        """ create a new order after payment """
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "not autorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        request.data["user"] = user_id


        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            order_id = response.data.get("id")
            self.comvert_cart_items_to_order_items(user_id, order_id)

        notificatio_description = f"you have created a new order today at {datetime.datetime.now()}"
        notification_message = "your order placed successfully"

        self.create_notification(user_id, notification_message, notificatio_description)
        
        return response
    
    @action(detail=True, methods=["put"], url_path="update_progress")
    def update_progress(self, request, *args, **kwargs):
        """ update progress of the order """
        progress = request.data.get("progress")
        order_id = kwargs.get("pk")
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "not autorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if not progress:
            return Response({"error": "no progress"}, status=status.HTTP_401_UNAUTHORIZED)
    
        order = get_object_or_404(Orders, id=order_id)

        order.progress = progress
        order.save()

        notification_message = f"order {progress}"
        notification_description = f"your order progress has beed updated at{datetime.datetime.now()}"

        self.create_notification(user_id, notification_message, notification_description)
        return Response({"message": "order progress changed"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["put"], url_path="change_status")
    def change_status(self, request, *args, **kwargs):
        """ change status of the order """
        new_status = request.data.get("status")
        order_id = kwargs.get("pk")
        user_id = get_user_from_request(request).get("id")

        if not user_id:
            return Response({"error": "not autorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if not new_status:
            return Response({"error": "no status"}, status=status.HTTP_401_UNAUTHORIZED)
        
        order = get_object_or_404(Orders, id=order_id)

        order.status = new_status
        order.save()

        notification_message = f"order {status}"
        notification_description = f"your order status has beed updated at{datetime.datetime.now()}"
        self.create_notification(user_id, notification_message, notification_description)
        return Response({"message": "order status changed"}, status=status.HTTP_200_OK)




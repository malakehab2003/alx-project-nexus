from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Payment
from ..serialzers import PaymentSerializer
from ..utils.authentication import get_user_from_request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



class PaymentViewSet(viewsets.ModelViewSet):
    """ ViewSet for the Payment model """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Returns Payments belonging to the authenticated user """
        user_id = get_user_from_request(self.request).get("id")
        if not user_id:
            return Payment.objects.none()
        return Payment.objects.filter(user=user_id)
    
    def create(self, request, *args, **kwargs):
        """ update create payment """
        user_id = get_user_from_request(request).get("id")
        last4 = request.data.get("last4")

        if len(last4) != 4:
            return Response({"error": "last4 should be 4 digits"}, status=status.HTTP_400_BAD_REQUEST)

        request.data["user"] = user_id

        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """ update the update payment api """
        user_id = get_user_from_request(request).get("id")
        last4 = request.data.get("last4")

        if len(last4) != 4:
            return Response({"error": "last4 should be 4 digits"}, status=status.HTTP_400_BAD_REQUEST)

        request.data["user"] = user_id

        return super().update(request, *args, **kwargs)

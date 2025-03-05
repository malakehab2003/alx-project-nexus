from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ..models import PromoCode
from ..serialzers import PromoCodeSerializer
from ..utils.authentication import get_user_from_request
from django.shortcuts import get_object_or_404

User = get_user_model()

class PromoCodeViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """ ViewSet for the PromoCode model """
    serializer_class = PromoCodeSerializer
    lookup_field = "id"
    queryset = PromoCode.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Returns Promocodes belonging to the authenticated user """
        user_id = get_user_from_request(self.request).get("id")
        if not user_id:
            return PromoCode.objects.none()
        return PromoCode.objects.filter(user=user_id)
    
    @action(detail=True, methods=['post'], url_path="apply_code")
    def apply_promo_code(self, request, *args, **kwargs):
        """ apply the promocode """
        try:
            price = float(request.data.get("price", 0))
        except (ValueError, TypeError):
            return Response({"error": "Invalid price format"}, status=status.HTTP_400_BAD_REQUEST)
        
        if price <= 0:
            return Response({"error": "Price must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

        promo_code_id = kwargs.get("id")
        user_id = get_user_from_request(request).get("id")

        if not price or not user_id:
            return Response({"error": "no price to use promocode"}, status=status.HTTP_400_BAD_REQUEST)
        
        promo_code = get_object_or_404(PromoCode, id=promo_code_id)

        if getattr(promo_code.user, "id", None) == user_id:
            discounted_price = price - ((price * promo_code.discount) / 100)
            return Response({"price after discount": discounted_price}, status=status.HTTP_200_OK)
        return Response({"error": "cannot apply promo code"}, status=status.HTTP_400_BAD_REQUEST)
    

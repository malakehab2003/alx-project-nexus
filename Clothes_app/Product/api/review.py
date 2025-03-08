from ..models import Review, Product, Image
from User.models import User
from ..serialzers import ReviewSerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from User.utils.authentication import get_user_from_request
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class ReviewViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """ViewSet for the Review model."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def calculte_final_rate(self, product_rate, new_rate):
        """ take the new rate and add to the rate of the product """
        if product_rate is None:
            return new_rate
        final_rate = (float(product_rate) + float(new_rate)) / 2
        return round(final_rate, 2)
    
    def validate_rate(self, rate):
        """ see if rate is validated """
        try:
            rate = float(rate)
        except ValueError:
            return None
        if 0 <= rate <= 5:
            return rate
        return None

    def create(self, request, *args, **kwargs):
        """ create a review """
        user_id = get_user_from_request(request).get("id")
        product_id = request.data.get("product_id")
        rate = request.data.get("rate")
        message = request.data.get("message")
        image = request.data.get("image")

        validated_rate = self.validate_rate(rate)

        if not validated_rate:
            return Response({"error": "rate should be between 0 and 5"}, status=status.HTTP_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        final_rate = self.calculte_final_rate(product.rate, rate)

        product.rate = final_rate
        product.save()

        review = Review.objects.create(
            user=user,
            product=product,
            rate=validated_rate,
            message=message,
            image=image
        )

        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

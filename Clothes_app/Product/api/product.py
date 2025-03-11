from rest_framework import viewsets, mixins
from django.db.models import Q
from ..models import Product
from ..serialzers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ ViewSet for filtering products based on sale, gender, price, search, review, and brand. """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter products based on query parameters."""
        queryset = Product.objects.all()
        sale_filter = self.request.query_params.get("on_sale", None)
        gender_filter = self.request.query_params.get("gender", None)
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        search_query = self.request.query_params.get("search", None)
        review_filter = self.request.query_params.get("review", None)
        brand_filter = self.request.query_params.getlist("brand", None)  # Accept multiple brands
        category_filter = self.request.query_params.getlist("category", None)  # Accept multiple categories

        # Filter by Sale
        if sale_filter is not None:
            queryset = queryset.filter(sale__gt=0)

        # Filter by Gender
        if gender_filter:
            if gender_filter.lower() == "male":
                queryset = queryset.filter(Q(gender="male") | Q(gender="both"))
            elif gender_filter.lower() == "female":
                queryset = queryset.filter(Q(gender="female") | Q(gender="both"))

        # Filter by Price Range
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Search Filter (matches name and category)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(category__name__icontains=search_query)  # Assuming category has a 'name' field
            )

        # Filter by Review
        if review_filter:
            queryset = queryset.filter(rate__gte=review_filter)

        # Filter by Brand (if brand API exists, get intersection)
        if brand_filter:
            queryset = queryset.filter(brands__in=brand_filter)

        # Filter by Category (allow multiple categories)
        if category_filter:
            queryset = queryset.filter(category__in=category_filter)

        return queryset

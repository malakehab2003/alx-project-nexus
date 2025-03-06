from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.product import ProductViewSet
from .api.category import CategoryViewSet
from .api.brand import BrandViewSet

router = DefaultRouter()
router.register("product", ProductViewSet)
router.register("category", CategoryViewSet)
router.register("brand", BrandViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

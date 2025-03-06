from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.product import ProductViewSet
from .api.category import CategoryViewSet

router = DefaultRouter()
router.register("product", ProductViewSet)
router.register("category", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.product import ProductViewSet
from .api.category import CategoryViewSet
from .api.brand import BrandViewSet
from .api.image import ImageViewSet
from .api.review import ReviewViewSet

router = DefaultRouter()
router.register("product", ProductViewSet)
router.register("category", CategoryViewSet)
router.register("brand", BrandViewSet)
router.register("image", ImageViewSet)
router.register("review", ReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.user import UserViewSet
from .api.address import AddressViewSet
from .api.promocode import PromoCodeViewSet

router = DefaultRouter()
router.register("user", UserViewSet)
router.register("address", AddressViewSet)
router.register("promocode", PromoCodeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

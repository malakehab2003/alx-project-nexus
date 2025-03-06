from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.user import UserViewSet
from .api.address import AddressViewSet
from .api.promocode import PromoCodeViewSet
from .api.notification import NotificationViewSet
from .api.payment import PaymentViewSet

router = DefaultRouter()
router.register("user", UserViewSet)
router.register("address", AddressViewSet)
router.register("promocode", PromoCodeViewSet)
router.register("notification", NotificationViewSet)
router.register("payment", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

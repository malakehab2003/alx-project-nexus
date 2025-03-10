from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.cart import CartViewSet
from .api.cart_items import CartItemsViewSet
from .api.wishlist import WishlistViewSet
from .api.orders import OrdersViewSet

router = DefaultRouter()
router.register("cart", CartViewSet)
router.register("cart_item", CartItemsViewSet)
router.register("wishlist", WishlistViewSet)
router.register("order", OrdersViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

from django.contrib import admin

# Register your models here.
from .models import Cart, Wishlist, Orders, OrderItem

admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Orders)
admin.site.register(OrderItem)

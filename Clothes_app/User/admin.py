from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, Notification, PromoCode

# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Notification)
admin.site.register(PromoCode)

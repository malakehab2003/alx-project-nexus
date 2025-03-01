from django.contrib import admin
from .models import Product, Category, Brand, Image, Review, Color, Size

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Color)
admin.site.register(Size)

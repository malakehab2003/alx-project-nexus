from django.db import models
from User.models import Payment, User, Address, PromoCode
from Product.models import Product, Color, Size

# Create your models here.

class Cart(models.Model):
    """ Create a card model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.name} - Cart"
    
class CartItems(models.Model):
    """ Create cart items model """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)

    
class Wishlist(models.Model):
    """ Create a wishlist model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.user.name} - Wishlist"
    
class Orders(models.Model):
    """ Create an order model """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    SHIPPING_CHOICES = [
        ('economy', 'Economy'),
        ('regular', 'Regular'),
        ('express', 'Express'),
    ]
    shipping_type = models.CharField(max_length=10, choices=SHIPPING_CHOICES, default='regular')
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    PROGRESS_CHOICES = [
        ('order_placed', 'Order Placed'),
        ('in_progress', 'In Progress'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='order_placed')
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    payment_type = models.CharField(max_length=100, choices=Payment.PROVIDER_CHOICES)
    promoCode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.user.name} - Order"
    
class OrderItem(models.Model):
    """ Create an order items model """
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f"{self.order.user.name} - Order Items"

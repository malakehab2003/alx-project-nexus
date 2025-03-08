from django.db import models
from User.models import User

class Category(models.Model):
    """ Create a category model """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    """ Create a brand model """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    """ Create a product model """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('out_of_stock', 'Out_of_stock'),
        ('new', 'New'),
        ('popular', 'Popular'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sale = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('both', 'Both'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='both')

    brands = models.ManyToManyField(Brand, related_name="products", blank=True)
    category = models.ManyToManyField(Category, related_name="products", blank=True)

    def __str__(self):
        return self.name
    
    
class Image(models.Model):
    """ Create an image model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey('Review', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    
class Review(models.Model):
    """ Create a review model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=3, decimal_places=1)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.message
    
class Size(models.Model):
    """ Create a size model """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name
    
class Color(models.Model):
    """ Create a color model """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

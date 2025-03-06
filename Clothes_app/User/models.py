from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

def validateEmailPassword(email, password):
    """Validate email and password"""
    if not email:
        raise ValueError("Email is required")
    if not password:
        raise ValueError("Password is required")
    return email, password

class UserManager(BaseUserManager):
    """Custom user manager"""
    def create_user(self, email, password, **extra_fields):
        """Create and return a JWT"""
        email, password = validateEmailPassword(email, password)
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a JWT"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=False)
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female")]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField("auth.Group", related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="custom_user_permissions", blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name", "phone"]

    objects = UserManager()

    def __str__(self):
        """Return user name"""
        return self.name

class Address(models.Model):
    """Create an address model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return address name"""
        return f"{self.name} - {self.user.name}"
    
class PromoCode(models.Model):
    """Create a promo code model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="promo_codes")
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return promo code"""
        return self.code
    
class Notification(models.Model):
    """Create a notification model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return user name"""
        return f"{self.user.name} - Notification"
    
class Payment(models.Model):
    """Create a payment model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    PROVIDER_CHOICES = [
            ("stripe", "Stripe"),
            ("paypal", "Paypal"),
            ("google_pay", "Google Pay"),
            ("apple_pay", "Apple Pay"),
        ]
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    payment_id = models.CharField(max_length=100)
    last4 = models.DecimalField(max_digits=4, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return user name"""
        return f"{self.user.name} - Payment"

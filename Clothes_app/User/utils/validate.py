import re
from rest_framework.exceptions import ValidationError

def validate_args_not_none(*args):
    """Validate the arguments"""
    for arg in args:
        if not arg:
            raise ValidationError({"error": "Missing argument"})

def validate_email(email):
    """Validate the email"""
    if not email:
        raise ValidationError({"email": "Email is required"})
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError({"email": "Invalid email"})
    

def validate_password(password):
    """Validate the password"""
    if not password:
        raise ValidationError({"password": "Password is required"})
    if len(password) < 8:
        raise ValidationError({"password": "Password must be at least 8 characters long"})
    if not re.search(r"[A-Za-z0-9]", password):  # Ensure it contains alphanumeric characters
        raise ValidationError({"password": "Password must contain only alphanumeric characters"})
    if not re.search(r"[A-Za-z]", password):  # Ensure at least one letter exists
        raise ValidationError({"password": "Password must contain at least one letter"})
    if not re.search(r"[0-9]", password):  # Ensure at least one digit exists
        raise ValidationError({"password": "Password must contain at least one number"})
    if not re.search(r"[A-Z]", password):  # Ensure at least one uppercase letter exists
        raise ValidationError({"password": "Password must contain at least one uppercase letter"})
    if not re.search(r"[a-z]", password):  # Ensure at least one lowercase letter exists
        raise ValidationError({"password": "Password must contain at least one lowercase letter"})
    if not re.search(r"[^A-Za-z0-9]", password):  # Ensure at least one special character exists
        raise ValidationError({"password": "Password must contain at least one special character"})

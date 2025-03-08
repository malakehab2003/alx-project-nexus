import random
from ..tasks import send_verification_email

def create_verification_and_send_email(email):
    """Create a verification code and send an email"""
    verification_code = str(random.randint(1000, 9999))
    send_verification_email.delay(email, verification_code)
    return verification_code
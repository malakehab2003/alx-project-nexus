from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_verification_email(email, verification_code):
    """Generate and send a verification code asynchronously"""
    subject = "Your Verification Code"
    message = f"Your verification code is: {verification_code}"
    from_email = "lokaehab2003@gmail.com"

    send_mail(subject, message, from_email, [email])
    return "Email sent successfully"

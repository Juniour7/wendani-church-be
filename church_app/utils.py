from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(to_email, subject, message):
    """
    Send confirmation if user provided email
    """
    if not to_email:
        return 
    
    try:
        send_mail(
            subject = subject,
            message = message,
            from_email = settings.DEFAULT_FROM_EMAIL,
            receipient_list = [to_email],
            fail_security = True
        )

    except Exception as e:
        print(f"Email send failed: {e}")


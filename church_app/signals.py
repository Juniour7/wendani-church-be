from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

# Our models
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, BenevolenceForm, ContactForm

def format_instance_details(instance):
    """
    Helper function to loop through model fields and create a readable string.
    """
    details = []
    # Loop through all fields in the model
    for field in instance._meta.fields:
        field_name = field.verbose_name.title() # Gets readable name (e.g. "First Name")
        field_value = getattr(instance, field.name)
        
        # specific handling for choice fields to show the Label not the ID
        if hasattr(instance, f'get_{field.name}_display'):
            field_value = getattr(instance, f'get_{field.name}_display')()
            
        details.append(f"{field_name}: {field_value}")
    
    return "\n".join(details)

@receiver(post_save, sender=PrayerRequestForm)
@receiver(post_save, sender=BaptismRequestForm)
@receiver(post_save, sender=DedicationForm)
@receiver(post_save, sender=MembershipTransferForm)
@receiver(post_save, sender=BenevolenceForm)
@receiver(post_save, sender=ContactForm)
def send_submission_notification(sender, instance, created, **kwargs):
    """
    Sends an email when a new request is created.
    """
    if created: # Only send on creation, not on updates (like status changes)
        subject = f"New Submission: {instance._meta.verbose_name.title()}"
        
        # 1. Get all data details
        data_summary = format_instance_details(instance)
        
        # 2. Generate Frontend Link
        # Assuming your frontend uses IDs: https://portal.kahawawendanisda.org/requests/baptism/5
        # You might need to adjust the path string based on your actual React/Frontend routes
        model_name = instance._meta.model_name # e.g., 'baptismrequestform'
        link = f"{settings.FRONTEND_BASE_URL}"
        
        # Alternative: If using Django Admin link
        # link = f"{settings.FRONTEND_BASE_URL}/admin/your_app/{model_name}/{instance.id}/change/"

        message = (
            f"Hello,\n\n"
            f"A new {instance._meta.verbose_name} has been submitted.\n\n"
            f"--- DETAILS ---\n"
            f"{data_summary}\n"
            f"----------------\n\n"
            f"View full details here:\n{link}\n\n"
            f"Regards,\nKahawa Wendani SDA Portal"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFICATION_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error so the user request doesn't crash if email fails
            print(f"Failed to send email: {e}")
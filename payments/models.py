from django.db import models

# Create your models here.
class MpesaTransaction(models.Model):
    PURPOSE_CHOICES = [
        ('Tithe', 'Tithe'),
        ('Offering', 'Offering'),
        ('Local Church Budget (LCB)', 'Local Church Budget (LCB)'),
        ('Camp Offering', 'Camp Offering'),
        ('Camp Expenses', 'Camp Expenses'),
        ('Evangelism', 'Evangelism'),
        ('Station Dev', 'Station Dev'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    other_purpose_details = models.CharField(max_length=50, blank=True, null=True, help_text="If 'Other', please specify")
    checkout_request_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='PENDING')
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        # Display the selected purpose, or the other_purpose_details if 'Other' is chosen
        display_purpose = self.get_purpose_display()
        if self.purpose == 'Other' and self.other_purpose_details:
            display_purpose = self.other_purpose_details
        return f"{self.name} - {self.amount} - {display_purpose}"

from django.db import models

# Create your models here.
class MpesaTransaction(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    checkout_request_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING')
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        # Display the selected purpose, or the other_purpose_details if 'Other' is chosen
        display_purpose = self.get_purpose_display()
        if self.purpose == 'Other' and self.other_purpose_details:
            display_purpose = self.other_purpose_details
        return f"{self.name} - {self.amount} - {display_purpose}"


class MpesaPurpose(models.Model):
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

    transaction = models.ForeignKey(
        MpesaTransaction,
        related_name='purposes',
        on_delete=models.CASCADE
    )
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    other_purpose_details = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.purpose} - {self.amount}"

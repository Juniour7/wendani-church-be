from django.db import models
from .validators import validate_file_extension, valdate_file_size

# Models
class PrayerRequestForm(models.Model):
    """Prayer Request Form to store Prayer requests"""
    ACTION = [
        ('read', 'Read' ),
        ('unread', 'Unread' ),
    ]
    REQUEST_TYPE = [
        ('personal request', 'personal request' ),
        ('family request', 'family request' ),
        ('health & healing', 'health & healing' ),
        ('guidance & direction', 'guidance & direction' ),
        ('thanksgiving', 'thanksgiving' ),
        ('other', 'other' ),
    ]
    full_name = models.CharField(max_length=200, blank=True, null=True) #optional
    email = models.EmailField(blank=True, null=True) #optional
    phone_number = models.CharField(max_length=15, blank=True, null=True) #optional
    prayer_type = models.CharField(max_length=200, choices=REQUEST_TYPE, default='personal request')
    prayer_request = models.TextField()
    status = models.CharField(max_length=150, choices=ACTION, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.full_name or f"Prayer Request #{self.id}"
    


class BaptismRequestForm(models.Model):
    """Baptismal Table to store Baptismal Requests"""
    ACTION = [
        ('read', 'Read' ),
        ('unread', 'Unread' ),
    ]
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True) #optional
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField()
    is_baptised = models.BooleanField(default=False)
    is_study = models.BooleanField(default=False)
    additional_information = models.TextField(blank=True) #optional
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=150, choices=ACTION, default='unread')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.full_name
    


class DedicationForm(models.Model):
    """Dedication Table to store Child Dedication Requests """
    GENDER_CHOICE = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    ACTION = [
        ('read', 'Read' ),
        ('unread', 'Unread' ),
        ('completed', 'Completed' ),
    ]
    child_full_name = models.CharField(max_length=200)
    date_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, default='male')
    father_full_name = models.CharField(max_length=200)
    father_email = models.EmailField(blank=True)
    father_phone_number = models.CharField(max_length=15)
    mother_full_name = models.CharField(max_length=200)
    mother_email = models.EmailField(blank=True)
    mother_phone_number = models.CharField(max_length=15)
    additional_information = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=150, choices=ACTION, default='unread')

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.child_full_name
    

class MembershipTransferForm(models.Model):
    """Membership Tranfer Table to Handle Membership Transfers"""
    PROCESS_STATUS = [
        ("pending" , "Pending"),
        ("completed" , "completed"),
        ("failed" , "Failed"),
    ]
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15) 
    date_of_birth = models.DateField()
    physical_address = models.CharField(max_length=100, blank=True)
    from_church_name = models.CharField(max_length=200)
    from_district_name = models.CharField(max_length=200)
    from_conference_name = models.CharField(max_length=200)
    from_address = models.CharField(max_length=200)
    to_church_name = models.CharField(max_length=200)
    to_district_name = models.CharField(max_length=200)
    to_conference_name = models.CharField(max_length=200)
    to_address = models.CharField(max_length=200)
    additional_notes = models.TextField(blank=True)
    board_minute_number = models.CharField(max_length=100)
    first_reading_date = models.DateField()
    second_reading_date = models.DateField()
    business_number = models.CharField(max_length=100)
    status = models.CharField(max_length=150, choices=PROCESS_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.full_name
    

class ChurchMembers(models.Model):
    """Church Members Table"""
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(blank=True)
    membership_number = models.IntegerField()


class Events(models.Model):
    """Events Table To Handle Church Events"""
    DEPARTMENT_CHOICES = [
        ('Sabbath School' , 'Sabbath School'),
        ('AYS' , 'Youth Ministries'),
        ('CM' , 'Children’s Ministries'),
        ('FL' , 'Family Life'),
        ('AWM' , 'Adventist Women’s Ministries'),
        ('AMM' , 'Adventist Men’s Ministries'),
        ('HM' , 'Health Ministries'),
        ('ED' , 'Education'),
        ('STW' , 'Stewardship'),
        ('PARL' , 'Public Affairs & Religious Liberty'),
        ('PUB' , 'Publishing'),
        ('COM' , 'Communication'),
        ('PCM' , 'Public Campus Ministries'),
        ('ADV' , 'Adventurers'),
        ('MUS' , 'Music'),
        ('DEA' , 'Deacons'),
    ]
    title = models.CharField(max_length=200)
    date = models.DateField()
    venue = models.CharField(max_length=200)
    description = models.TextField()
    time = models.TimeField()
    department = models.CharField(max_length=200, choices=DEPARTMENT_CHOICES)
    image = models.ImageField(upload_to='events/')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title


class BenevolenceForm(models.Model):
    """Bennevolence Table to Habdle Benevolence Registrations"""
    REGISTRATION_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    ]

    MEMBERSHIP_STATUS = [
        ('visitor', 'Visitor'),
        ('church_member', 'Church Member'),
        ('sabbath_school_member', 'Sabbath School Member'),
    ]

    head_full_name = models.CharField(max_length=200)
    head_phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    membership_status = models.CharField(max_length=200, choices=MEMBERSHIP_STATUS)
    spouse_name = models.CharField(max_length=200, blank=True)
    church_name = models.CharField(max_length=200, blank=True)
    additional = models.TextField(blank=True)
    status = models.CharField(max_length=150, choices=REGISTRATION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.head_full_name

class Dependents(models.Model):
    """Each Benevolence Form can have multiple dependents"""
    benevolence_form = models.ForeignKey(BenevolenceForm, on_delete=models.CASCADE, related_name='dependents')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField()
    relationship = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class ContactForm(models.Model):
    """Contact Form to handle messages from users"""
    ACTION = [
        ('contacted', 'Contacted' ),
        ('unread', 'Unread' ),
    ]
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=150, choices=ACTION, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.full_name


class Announcements(models.Model):
    file = models.FileField(
        upload_to='announcements/',
        validators=[validate_file_extension, valdate_file_size]
    )
    description = models.TextField()
    title = models.CharField(max_length=200)
    size = models.PositiveIntegerField(editable=False, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.file and not self.size:
            self.size = self.file.size  # get size in bytes
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.title
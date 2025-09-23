from django.db import models

# Create your models here.
class PrayerRequestForm(models.Model):
    """Prayer Request Form to store Prayer requests"""
    REQUEST_TYPE = [
        ('personal request', 'personal request' ),
        ('family request', 'family request' ),
        ('health & healing', 'health & healing' ),
        ('guidance & direction', 'guidance & direction' ),
        ('thanksgiving', 'thanksgiving' ),
        ('other', 'other' ),
    ]
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField()
    prayer_type = models.CharField(max_length=200, choices=REQUEST_TYPE, default='personal request')
    prayer_request = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.full_name
    


class BaptismRequestForm(models.Model):
    """Baptismal Table to store Baptismal Requests"""
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField()
    date_of_birth = models.DateField()
    is_baptised = models.BooleanField(default=False)
    is_study = models.BooleanField(default=False)
    additional_information = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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
    child_full_name = models.CharField(max_length=200)
    date_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, default='male')
    father_full_name = models.CharField(max_length=200)
    father_email = models.EmailField()
    father_phone_number = models.IntegerField()
    mother_full_name = models.CharField(max_length=200)
    mother_email = models.EmailField()
    mother_phone_number = models.IntegerField()
    additional_information = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.child_full_name



class MembershipTransferForm(models.Model):
    """Membership Tranfer Table to Handle Membership Transfers"""
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField() 
    date_of_birth = models.DateField()
    physical_address = models.CharField(max_length=100)
    from_church_name = models.CharField(max_length=200)
    from_district_name = models.CharField(max_length=200)
    from_conference_name = models.CharField(max_length=200)
    from_address = models.CharField(max_length=200)
    to_church_name = models.CharField(max_length=200)
    to_district_name = models.CharField(max_length=200)
    to_conference_name = models.CharField(max_length=200)
    to_address = models.CharField(max_length=200)
    additional_notes = models.TextField()
    board_minute_number = models.IntegerField()
    first_reading_date = models.DateField()
    second_reading_date = models.DateField()
    business_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.full_name

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
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

class BenevolenceForm(models.Model):
    """Bennevolence Table to Habdle Benevolence Registrations"""
    MEMBERSHIP_STATUS = [
        ('Visitor', 'Visitor'),
        ('Registerd Member', 'Registerd Member'),
        ('Sabbath School Member', 'Sabbath School Member'),
    ]
    head_full_name = models.CharField(max_length=200)
    head_phone_number = models.IntegerField()
    email = models.EmailField()
    membership_status = models.CharField(max_length=200, choices=MEMBERSHIP_STATUS)
    spuse_name = models.CharField(max_length=200)
    church_name = models.CharField(max_length=200)
    dependents_name = models.CharField(max_length=200)
    dependents_number = models.IntegerField()
    dependents_relationship = models.CharField(max_length=200)
    additional = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.head_full_name


class ContactForm(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.full_name


class Announcements(models.Model):
    file = models.FileField()
    description = models.TextField
    title = models.CharField(max_length=200)
    uploaded_date = models.DateField()
    size = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.title
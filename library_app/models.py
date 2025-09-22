from django.db import models

# Create your models here.
class Book(models.Model):
    CATEGORY_CHOICE = [
        ('Prophecy', 'Prophecy'),
        ('Biograpy', 'Biograpy'),
        ('Health', 'Health'),
        ('Christian Living', 'Christian Living'),
        ('Education', 'Education'),
        ('Spiritual Growth', 'Spiritual Growth'),
        ('Bible Study', 'Bible Study'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICE)
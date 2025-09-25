from django.db import models

# Create your models here.
class Author(models.Model):
    """Table Of Blog Authors"""
    full_name = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    email = models.EmailField(blank=True, null=True)


class Blog(models.Model):
    """Table of BlogPosts"""
    CATEGORIES_CHOICES = [
        ('Faith', 'Faith'),
        ('Prayer', 'Prayer'),
        ('Doctrine', 'Doctrine'),
        ('Spiritual Growth', 'Spiritual Growth'),
        ('Stewardship', 'Stewardship'),
        ('Community', 'Community'),
        ('Prophecy', 'Prophecy'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=CATEGORIES_CHOICES)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    """Table of Comments"""
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
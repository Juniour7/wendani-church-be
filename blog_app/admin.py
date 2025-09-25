from django.contrib import admin
from .models import Author, Blog, Comments


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'content', 'author', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'category', 'created_at')
    search_fields = ('title', 'author')
from django.shortcuts import render
from .models import Blog, Author
from .serializers import BlogSerializer, AuthorSerializer
from rest_framework import viewsets

# Create your views here.
class BlogAPIView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        # Only return verified blogs for GET requests
        if self.request.method == 'GET':
            return Blog.objects.filter(is_verified=True)
        return Blog.objects.all()

class AuthorAPIView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
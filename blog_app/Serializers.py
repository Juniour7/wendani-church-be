from rest_framework import serializers

from .models import Author, Blog, Comments


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'full_name', 'phone_number', 'email']

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(max_length=200)
    class Meta:
        model = Comments
        fields = '__all__'

    def create(self, validated_data):
        return Comments(**validated_data)
    
    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance



class BlogSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True,required=False)
    author = AuthorSerializer()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'author', 'category', 'content', 'comments', 'created_at', 'is_verified']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author, created = Author.objects.get_or_create(**author_data)
        blog = Blog.objects.create(author = author, **validated_data)
        return blog




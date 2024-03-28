from rest_framework import serializers
from authapp.serializers import MyUser
from .models import Blog, Like, Comment

class BlogSerializer(serializers.ModelSerializer):
    author = MyUser()

    class Meta:
        model = Blog
        fields = "__all__"

class LikesSerializer(serializers.ModelSerializer):
    user = MyUser()

    class Meta:
        model = Like
        fields = ['user', 'blog']

class CommentSerializer(serializers.ModelSerializer):
    user = MyUser()

    class Meta:
        model = Comment
        fields = ['user', 'blog', 'text', 'tags', 'created_at']
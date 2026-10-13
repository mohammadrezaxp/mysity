from rest_framework import serializers
from blog.models import Post, Category, Comments
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    comment = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'

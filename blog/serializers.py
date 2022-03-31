from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Category, Post, Tag
from user_info.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
        ]


class PostListSerializer(WritableNestedModelSerializer):
    category = CategorySerializer
    author = UserSerializer

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body",
            "excerpt",
            "category",
            "author",
            "views",
        ]


class PostRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    author = UserSerializer
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body",
            "excerpt",
            "views",
            "category",
            "author",
            "tags",
            "body",
        ]
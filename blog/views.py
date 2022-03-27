from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import Category, Post, Tag
from .serializers import (
    CategorySerializer, PostListSerializer, TagSerializer)


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    博客文章视图集

    list:
    返回博客文章列表

    retrieve:
    返回博客文章详情

    list_comments:
    返回博客文章下的评论列表
    """

    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    # serializer_class_table = {
    #     "list": PostListSerializer,
    #     "retrieve": PostRetrieveSerializer,
    # }
    #
    # def get_serializer_class(self):
    #     return self.serializer_class_table.get(
    #         self.action, super().get_serializer_class()
    #     )

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    博客文章分类视图集

    list:
    返回博客文章分类列表
    """

    serializer_class = CategorySerializer
    # 关闭分页
    pagination_class = None

    def get_queryset(self):
        return Category.objects.all().order_by("name")


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    博客文章标签视图集

    list:
    返回博客文章标签列表
    """

    serializer_class = TagSerializer
    # 关闭分页
    pagination_class = None

    def get_queryset(self):
        return Tag.objects.all().order_by("name")
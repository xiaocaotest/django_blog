from rest_framework import mixins, viewsets, permissions
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_extensions.key_constructor.bits import (
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    RetrieveSqlQueryKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

from .utils import UpdatedAtKeyBit
from .models import Category, Post, Tag
from .serializers import (
    CategorySerializer, PostListSerializer, TagSerializer)


class PostUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "post_updated_at"


class PostListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = PostUpdatedAtKeyBit()


class PostObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = PostUpdatedAtKeyBit()


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    博客接口
    """

    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    @cache_response(timeout=5 * 60, key_func=PostListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(timeout=5 * 60, key_func=PostObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    分类接口
    """

    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    # 关闭分页
    pagination_class = None

    def get_queryset(self):
        return Category.objects.all().order_by("name")


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    标签接口
    """

    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 关闭分页
    pagination_class = None

    def get_queryset(self):
        return Tag.objects.all().order_by("name")
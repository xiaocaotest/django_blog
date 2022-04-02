from datetime import datetime

from django.apps import apps
from django.core.cache import cache
from django.urls import reverse
from django.utils.timezone import utc
from rest_framework import status
from rest_framework.test import APITestCase

from user_info.models import UserInfo
from blog.models import Category, Post, Tag
from blog.serializers import (
    PostListSerializer,
    PostRetrieveSerializer,
)


class PostViewSetTestCase(APITestCase):
    def setUp(self):
        # 断开 haystack 的 signal，测试生成的文章无需生成索引
        # apps.get_app_config("haystack").signal_processor.teardown()
        # 清除缓存，防止限流
        cache.clear()

        # 设置博客数据
        # post3 category2 tag2 2020-08-01 comment2 comment1
        # post2 category1 tag1 2020-07-31
        # post1 category1 tag1 2020-07-10
        user = UserInfo.objects.create_superuser(
            username="admin", email="admin@qq.com", password="admin"
        )
        self.cate1 = Category.objects.create(name="category1")
        self.cate2 = Category.objects.create(name="category2")
        self.tag1 = Tag.objects.create(name="tag1")
        self.tag2 = Tag.objects.create(name="tag2")

        self.post1 = Post.objects.create(
            title="title1",
            body="post1",
            category=self.cate1,
            author=user,
            created_time=datetime(year=2020, month=7, day=10).replace(tzinfo=utc),
        )
        self.post1.tags.add(self.tag1)

        self.post2 = Post.objects.create(
            title="title2",
            body="post2",
            category=self.cate1,
            author=user,
            created_time=datetime(year=2020, month=7, day=31).replace(tzinfo=utc),
        )
        self.post2.tags.add(self.tag1)

        self.post3 = Post.objects.create(
            title="title3",
            body="post3",
            category=self.cate2,
            author=user,
            created_time=datetime(year=2020, month=8, day=1).replace(tzinfo=utc),
        )
        self.post3.tags.add(self.tag2)

    def test_list_post(self):
        url = reverse("v1:post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PostListSerializer(
            instance=[self.post3, self.post2, self.post1], many=True
        )
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_post(self):
        url = reverse("v1:post-detail", kwargs={"pk": self.post1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PostRetrieveSerializer(instance=self.post1)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_nonexistent_post(self):
        url = reverse("v1:post-detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
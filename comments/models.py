from django.db import models
from django.utils import timezone


class Comment(models.Model):
    email = models.EmailField("邮箱")
    text = models.TextField("内容")
    created_time = models.DateTimeField("创建时间", default=timezone.now)
    post = models.ForeignKey("blog.Post", verbose_name="文章", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ["-created_time"]
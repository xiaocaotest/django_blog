from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    first_name = None
    last_name = None
    nick_name = models.CharField('昵称', max_length=50, default='')

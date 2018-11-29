from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.authtoken.models import Token as DefaultTokenModel

from .utils import import_callable

# Register your models here.

TokenModel = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))

# 通过AbstractUser 拓展 User 字段
class UserProfile(AbstractUser):
    nickName = models.CharField(max_length=30, null=True, blank=True, verbose_name='昵称')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='电话号码')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮箱')
    permissions = models.IntegerField(default=1, blank=True, verbose_name='用户权限')
    isDelete = models.BooleanField(default=False, verbose_name='是否注销')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

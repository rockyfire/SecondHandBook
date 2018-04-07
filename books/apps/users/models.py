from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    """
    用户信息
    """
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    faceimg = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    point = models.IntegerField(default=100,verbose_name="积分")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # name设置为可为空 使用username
    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    faceimg = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    point = models.IntegerField(default=100, verbose_name="积分")

    # 未实现的字段
    # last_login_ip = models.GenericIPAddressField("最近一次登陆IP", unpack_ipv4=True, blank=True, null=True)
    # ip_register = models.GenericIPAddressField("注册IP", unpack_ipv4=True, blank=True, null=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # name设置为可为空 使用username
    def __str__(self):
        return self.username


# from util import utils
# from django.contrib.auth.signals import user_logged_in
#
#
# # 未实现的功能
# def update_last_login_ip(sender, user, request, **kwargs):
#     """
#     Update the value of last_login_ip whenever a user logged in successfully
#     :param sender:
#     :param user:
#     :param request:
#     :param kwargs:
#     :return:
#     """
#     ip = utils.get_ip_address_from_request(request)
#     if ip:
#         user.last_login_ip = ip
#         user.save()
#
#
# user_logged_in.connect(update_last_login_ip)


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

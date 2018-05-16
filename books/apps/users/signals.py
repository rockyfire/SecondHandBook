# !/usr/bin/env python3
# *coding:utf-8* 
__author__ = 'rockyfire'

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()

# 后台用户和普通用户都会被这个信号量加密。然后后台用户就被加密两次了

# 我们的model对象进行操作的时候，会发出全局的信号。捕捉之后做出我们自己的操作。
# 参数一接收哪种信号，参数二是接收哪个model的信号
# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
# 	if created:
# 		instance.set_password(instance.password)
# 		instance.save()

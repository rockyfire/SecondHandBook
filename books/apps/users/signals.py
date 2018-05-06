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
# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
# 	if created:
# 		instance.set_password(instance.password)
# 		instance.save()

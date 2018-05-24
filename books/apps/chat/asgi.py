# -*- coding: utf-8 -*-
# @Author  : Rockyfire
# @Time    : 2018/5/21 15:27
import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")
channel_layer = channels.asgi.get_channel_layer()
# -*- coding: utf-8 -*-
# @Author  : Rockyfire
# @Time    : 2018/5/21 17:38

from django.conf.urls import url
from . import consumers
websocket_urlpatterns=[
    url(r'^ws/chat/(?P<room_name_json>[^/]+)/$', consumers.ChatConsumer),
]
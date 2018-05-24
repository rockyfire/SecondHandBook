# -*- coding: utf-8 -*-
# @Author  : Rockyfire
# @Time    : 2018/5/21 17:36
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions
from channels.http import AsgiRequest
from asgiref.sync import async_to_sync
from channels.auth import login
from django.contrib.auth import get_user_model

User = get_user_model()

import jwt
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

import logging
from .models import Room

logger = logging.getLogger(__name__)  # 为loggers中定义的名称

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class ChatConsumer(AsyncWebsocketConsumer):
    # def __init__(self):
    #     self.room_name = ''
    #     self.room_group_name = ''

    async def websocket_connect(self, message):
        # self.user = self.scope['user']
        self.label = self.scope['path']
        self.room_name = self.scope['url_route']['kwargs']['room_name_json']
        self.room_group_name = 'chat_%s' % self.room_name

        roomobj = Room.objects.get(name=self.room_name)
        roomobj.label = self.label
        roomobj.save()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        username = self.scope['cookies'].get('name', None)
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        text_data_json['handle'] = username
        roomobj = Room.objects.get(name=self.room_name)
        m = roomobj.messages.create(**text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'handle': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        handle = event['handle']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'handle': handle,
        }))

    def token_authenticate(self, token, message):
        """
        Tries to authenticate user based on the supplied token. It also checks
        the token structure and validity.
        """

        payload = self.check_payload(token=token, message=message)
        user = self.check_user(payload=payload, message=message)

        """Other authenticate operation"""
        return user, token

    # 检查负载
    def check_payload(self, token, message):
        payload = None
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            logger.warn(msg)
            # raise ValueError(msg)
            self._close_reply_channel(message)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            logger.warn(msg)
            self._close_reply_channel(message)
        return payload

    # 检查用户
    def check_user(self, payload, message):
        username = None
        try:
            username = payload.get('username')
        except Exception:
            msg = _('Invalid payload.')
            logger.warn(msg)
            self._close_reply_channel(message)
        if not username:
            msg = _('Invalid payload.')
            logger.warn(msg)
            self._close_reply_channel(message)
            return
            # Make sure user exists
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _("User doesn't exist.")
            logger.warn(msg)
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            logger.warn(msg)
            raise exceptions.AuthenticationFailed(msg)
        return user

    # 关闭websocket
    def _close_reply_channel(self, message):
        message.reply_channel.send({"close": True})

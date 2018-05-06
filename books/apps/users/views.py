from django.shortcuts import render

# Create your views here.
from random import choice
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializer import UserRegSerializer, SmsSerializer, UserDetailSerializer, ModifyPasswordSerializer
from .models import VerifyCode, UserProfile
from util.SendMSM import SendMessage
from Book.settings import ACCOUNT_SID, TOKEN

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class SmsCodeViewset(mixins.CreateModelMixin, GenericViewSet):
    """
        发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "123456789"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        """
        重写CreateModelMixin的crate
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        # raise_exception=True  错误就抛异常不会进入接下来的操作
        serializer.is_valid(raise_exception=True)

        # dict
        mobile = serializer.validated_data['mobile']
        code = self.generate_code()
        # 调用工具类的SendMessage
        sendmessage = SendMessage(ACCOUNT_SID, TOKEN)
        sms_status = sendmessage.send_sms(code=code, mobile=mobile)

        if sms_status['respCode'] != "00000":
            return Response({
                "mobile": sms_status['respDesc']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode.objects.filter(mobile=mobile)
            if code_record:
                code_record.update(code=code)
            else:
                code_record = VerifyCode(code=code, mobile=mobile)
                code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class CustomBackend(ModelBackend, GenericViewSet):

    def authenticate(self, username=None, password=None, **kwargs):
        """
        自定义用户验证 要重写authenticate
        可以使用手机号或用户名登录
        :param username:
        :param password:
        :param kwargs:
        :return:
        """

        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))

            # 用户名（手机号） 密码登录  手机号 验证码登录
            if user.check_password(password) or \
                    VerifyCode.objects.filter(mobile=username)[0].code == password:
                return user

        except (AttributeError, UserProfile.DoesNotExist) as e:
            raise serializers.ValidationError("该用户名未注册")
        except Exception as e:
            return serializers.ValidationError('请联系客服')


class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  GenericViewSet):
    """
        用户(注册|获取用户详细信息)
    """
    # serializer_class = UserRegSerializer
    # queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        """
        ViewSetMixin
        For example, to create a concrete view binding the 'GET' and 'POST' methods
        to the 'list' and 'create' actions...
        :return:
        """
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    # 无论用户传递怎样的用户ID，后台只返回当前的用户
    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 保存后获取user
        user = self.perform_create(serializer)
        # 未实现的功能
        # from util import utils
        # ip = utils.get_ip_address_from_request(request)
        # if ip:
        #     user.ip_register = ip
        re_dict = serializer.data

        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['username'] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

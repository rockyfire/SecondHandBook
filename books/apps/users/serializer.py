#!/usr/bin/env python3
# *_* coding:utf-8 *_*
# author:zkerpy

import re
from datetime import datetime
from datetime import timedelta
from rest_framework import serializers
from Book.settings import REGEX_MOBILE

from .models import VerifyCode, UserProfile
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
        发送短信验证码之前的验证操作
    """

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :return:
        """
        # 手机号是否已注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("手机号已注册")

        # 手机号格式是否正确
        if re.match(mobile, REGEX_MOBILE):
            raise serializers.ValidationError("手机格式不正确")

        # 验证码发送时间间隔
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

        # 当前时间大于一分钟之前的时间才可以再次发送请求
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送不足一分钟，请稍后")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化
    """

    class Meta:
        model = User
        fields = ('name', 'mobile')


class UserRegSerializer(serializers.ModelSerializer):
    # 验证码是用户Model中没有的字段
    # 使用方法和forms.CharField类似
    # 必填 最大长度 最小长度 只写 表单提示语 错误提示Error_messages
    # 允许空白 验证 唯一验证
    # 输入类型
    code = serializers.CharField(required=True,
                                 max_length=4,
                                 min_length=4,
                                 write_only=True,
                                 help_text="验证码",
                                 label='验证码',
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "必填字段",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 })
    # 用户名
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="该用户已经存在")])
    # 密码
    password = serializers.CharField(style={
        'input_type': 'password'
    }, label='密码', write_only=True, )

    """
        重写create 设置密码
    """

    # def create(self,validated_data):
    #     # 创建成功后可以取到User
    #     user=super(UserRegSerializer, self).create(validated_data=validated_data)
    #     # user继承AbstractUser，AbstractUser继承AbstractBaseUser 调用AbstractBaseUser的
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # try:
        #     verify_records=VerifyCode.objects.get(mobile=self.initial_data['username'],code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # initial_data[] 前端传递过来的值

        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            # 最近的一次验证码
            last_recodes = verify_records[0]
            # 五分钟之前的时间
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 保证在五分钟之内
            if five_mintes_ago > last_recodes.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_recodes.code != code:
                raise serializers.ValidationError('验证码错误')

        # return code
        else:
            raise serializers.ValidationError('手机号未注册')

    # 全局的校验 重写Serializer的validate
    def validate(self, attrs):
        # 用户名字段赋值给手机字段
        attrs['mobile'] = attrs['username']
        # 删除验证码，Model没有验证码这个字段
        del attrs['code']
        # 返回
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')


from django.db.models import Q


class ModifyPasswordSerializer(serializers.ModelSerializer):
    def validate_password(self, code):
        user = User.objects.get(Q(username=self.initial_data['username']) | Q(mobile=self.initial_data['username']))
        if user.check_password(self.initial_data['old_password']):
            if self.initial_data['new_password'] == self.initial_data['confirm_password']:
                user.set_password(self.initial_data['new_password'])
            elif self.initial_data['new_password'] == self.initial_data['old_password']:
                raise serializers.ValidationError('原密码和新密码相同')
            else:
                raise serializers.ValidationError('请输入一致的密码')
        else:
            raise serializers.ValidationError('原密码错误')

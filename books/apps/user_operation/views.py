from django.shortcuts import render

# Create your views here
from rest_framework import mixins, viewsets
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializer import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer, UserAddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from util.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve：
        收藏商品详情
    create：
        收藏商品
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 改变搜索字段，retrieve默认返回搜索字段是主键id，但要搜索的字段是books中的id。
    lookup_field = "books_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        if self.action == "create":
            return UserFavSerializer
        return UserFavSerializer
    # 扩展功能
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     books = instance.books
    #     books.fav_num += 1
    #     books.save()

    # 未实践
    # def perform_destroy(self, instance):
    #     books = instance.books
    #     books.fav_num -=1
    #     books.save()
    #     instance.delete()


class UserLeavingMessageViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    retrieve：
        用户留言详情
    create：
        创建用户留言
    """
    serializer_class = UserLeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    list:
        获取地址
    retrieve：
        收货地址详情
    create：
        创建收货地址
    delete:
        删除收货地址
    """

    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

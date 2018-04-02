from django.shortcuts import render

# Create your views here
from rest_framework import mixins, viewsets
from rest_framework import permissions
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializer import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer, UserAddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class IsOwnerOrReadOnly(permissions.BasePermission):
    """

    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


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
    # queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer
    permissions_class = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    lookup_field = "books_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer


class UserLeavingMessageViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
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
    permissions_class = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    list:
        获取地址
    retrieve：
        用户地址详情
    create：
        创建用户地址
    delete:
        删除用户地址
    """

    serializer_class = UserAddressSerializer
    permissions_class = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

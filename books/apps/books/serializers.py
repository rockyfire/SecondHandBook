#!/usr/bin/env python3
# *_* coding:utf-8 *_*
# author:zkerpy

from rest_framework import serializers
from .models import BooksImage, Books, BooksCategory
from comment.serializer import BookCommentSerializer
from django.utils import timezone


# from comment.models import Comment

# BooksCategory
class CategorySerializer3(serializers.ModelSerializer):
    """
        商品类别序列化 三级类目
    """

    class Meta:
        model = BooksCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
        商品类别序列化 二级类目 二级分类嵌套三级分类 many=True表示二级分类有多个（必须设置）
    """
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = BooksCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
        商品类别序列化 一级类目 一级分类嵌套二级分类 many=True表示二级分类有多个（必须设置）
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = BooksCategory
        fields = "__all__"


# BooksImage

class BooksImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksImage
        fields = ("image",)


# Books
class BooksSerializer(serializers.ModelSerializer):
    """
    书籍序列化
    """
    images = BooksImageSerializer(many=True)
    comments = BookCommentSerializer(many=True)

    class Meta:
        model = Books
        fields = "__all__"

    # 验证前端传送过来的字段
    def create(self, validated_data):
        """
        Create and return a new Books instance,given the validate data
        :param validated_data:
        :return:
        """
        comment = validated_data["comment"]
        return Books.objects.create(**validated_data)


from datetime import timedelta


class BookCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    add_time = serializers.HiddenField(
        default=timezone.now
    )
    revoke = serializers.DateTimeField(
        initial=timezone.now() + timedelta(days=7),
        default=timezone.now() + timedelta(days=7),
    )

    category = serializers.PrimaryKeyRelatedField(required=True, queryset=BooksCategory.objects.filter(category_type=3))

    # def validate_revoke(self, value):
    #     """
    #     下架时间必须大于添加时间
    #     :param value:
    #     :return:
    #     """
    #     if value > timezone.now:
    #         raise serializers.ValidationError("下架时间必须大于添加时间")
    #     return value

    def validate(self, attrs):
        if attrs['add_time'] > attrs['revoke']:
            raise serializers.ValidationError("下架时间必须大于添加时间")
        return attrs

    class Meta:
        model = Books
        fields = '__all__'

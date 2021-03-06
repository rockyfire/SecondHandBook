#!/usr/bin/env python3
# *_* coding:utf-8 *_*
# author:zkerpy

from rest_framework import serializers
from .models import BooksImage, Books, BooksCategory, BooksBanner, BooksStatus
from comment.serializer import BooksCommentDetailSerializer
from users.serializer import UserInfoSerializer
from django.db.models import Q


class CategorySerializer3(serializers.ModelSerializer):
    """
        商品类别序列化 三级类目
    """

    class Meta:
        model = BooksCategory
        fields = "__all__"


class BooksImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksImage
        fields = ("image",)


class BooksSerializer(serializers.ModelSerializer):
    """
    书籍序列化
    """
    # ↓↓↓ 在models中自定义的related_name有关
    images = BooksImageSerializer(many=True)
    books_comment = BooksCommentDetailSerializer(many=True)
    user = UserInfoSerializer(many=False)

    class Meta:
        model = Books
        fields = '__all__'

    def create(self, validated_data):
        """
        验证前端传送过来的字段
        Create and return a new Books instance,given the validate data
        :param validated_data:
        :return:
        """
        # 添加评论
        comment = validated_data["comment"]
        return Books.objects.create(**validated_data)


class CategorySerializer2(serializers.ModelSerializer):
    """
        商品类别序列化 二级类目 二级分类嵌套三级分类 many=True表示二级分类有多个（必须设置）
    """
    sub_cat = CategorySerializer3(many=True)
    category_books = BooksSerializer(many=True)

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


class BookCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    category = serializers.PrimaryKeyRelatedField(required=True, queryset=BooksCategory.objects.filter(category_type=2))

    class Meta:
        model = Books
        exclude = ('add_time',)


class BookBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBanner
        fields = '__all__'


# 获取某个书籍状态下的所有书籍
class IndexStatusSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    def get_books(self, obj):
        status_books = Books.objects.filter(Q(status=obj.id))
        books_serializer = BooksSerializer(status_books, many=True, context={'request': self.context['request']}).data
        return books_serializer

    class Meta:
        model = BooksStatus
        fields = "__all__"

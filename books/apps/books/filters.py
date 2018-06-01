#!/usr/bin/env python3
# *_* coding:utf-8 *_*
# author:zkerpy

import django_filters

from .models import Books, BooksImage, BooksCategory
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class BooksFilter(django_filters.rest_framework.FilterSet):
    """
        书籍过滤类
    """
    # 最低价格
    price_min = django_filters.NumberFilter(name='price', lookup_expr='gte')
    # 最高价格
    price_max = django_filters.NumberFilter(name='price', lookup_expr='lte')
    # 查找该类型下的所有书籍
    top_category = django_filters.CharFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category=BooksCategory.objects.get(id=value)) | Q(category__parent_category_id=value))

    # 查找该用户下的所有书籍
    book_user = django_filters.Filter(method='book_user_filter')

    def book_user_filter(self, queryset, name, value):
        return queryset.filter(user=User.objects.filter(username=value))

    class Meta:
        model = Books
        fields = ['price_min', 'price_max', 'status', ]

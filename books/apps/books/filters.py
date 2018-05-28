#!/usr/bin/env python3
# *_* coding:utf-8 *_*
# author:zkerpy

import django_filters

from .models import Books, BooksImage,BooksCategory
from django.db.models import Q


class BooksFilter(django_filters.rest_framework.FilterSet):
    """
        书籍过滤类
    """
    price_min = django_filters.NumberFilter(name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='price', lookup_expr='lte')

    top_category = django_filters.CharFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category=BooksCategory.objects.get(id=value)) | Q(category__parent_category_id=value))

    # book_status = django_filters.NumberFilter(method='book_status_filter')
    #
    # def book_status_filter(self, queryset, name, value):
    #     return queryset.filter(Q(status=value))

    book_user = django_filters.Filter(method='book_user_filter')

    def book_user_filter(self, queryset, name, value):
        return queryset.filter(images=BooksImage.objects.filter(image=value))

    class Meta:
        model = Books
        fields = ['price_min', 'price_max', 'status', ]

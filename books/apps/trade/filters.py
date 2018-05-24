#!/usr/bin/env python3
# *_* coding:utf-8 *_*
# author:zkerpy

import django_filters

from .models import Books, OrderBooks, OrderInfo
from django.db.models import Q, QuerySet


class SoldBooksFilter(django_filters.rest_framework.FilterSet):
    """
        已卖出宝贝过滤类
    """
    class Meta:
        model = OrderBooks
        fields = ['add_time', ]

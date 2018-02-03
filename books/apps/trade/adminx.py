# -*- coding: utf-8 -*-
__author__ = 'bobby'

import xadmin
from .models import ShoppingCart, OrderInfo, OrderBooks


class ShoppingCartAdmin(object):
	list_display = ["user", "books", "nums", ]


class OrderInfoAdmin(object):
	list_display = ["user", "order_sn", "trade_no", "pay_status", "post_script", "order_mount",
					"order_mount", "pay_time", "add_time"]

	class OrderBooksInline(object):
		model = OrderBooks
		exclude = ['add_time', ]
		extra = 1
		style = 'tab'

	inlines = [OrderBooksInline, ]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)

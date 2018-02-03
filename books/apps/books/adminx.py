#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: liyao
@license: Apache Licence 
@contact: yli@posbao.net
@site: http://www.piowind.com/
@software: PyCharm
@file: adminx.py
@time: 2017/7/4 17:04
"""
import xadmin
from .models import Books


class BooksAdmin(object):
	list_display = ["name", "press", "version",
					"price", "buyoutprice", "ship_free",
					"photo", "nums", "revoke", "status", "add_time"]
	search_fields = ['name', ]
	list_filter = ["name", "nums", "market_price", "shop_price", "add_time"]
	style_fields = {"desc": "ueditor"}


# class GoodsImagesInline(object):
# 	model = GoodsImage
# 	exclude = ["add_time"]
# 	extra = 1
# 	style = 'tab'

# inlines = [GoodsImagesInline]


# class GoodsCategoryAdmin(object):
# 	list_display = ["name", "category_type", "parent_category", "add_time"]
# 	list_filter = ["category_type", "parent_category", "name"]
# 	search_fields = ['name', ]


# class GoodsBrandAdmin(object):
# 	list_display = ["category", "image", "name", "desc"]
#
# 	def get_context(self):
# 		context = super(GoodsBrandAdmin, self).get_context()
# 		if 'form' in context:
# 			context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
# 		return context
#
#
# class BannerGoodsAdmin(object):
# 	list_display = ["goods", "image", "index"]
#
#
# class HotSearchAdmin(object):
# 	list_display = ["keywords", "index", "add_time"]
#
#
# class IndexAdAdmin(object):
# 	list_display = ["category", "goods"]


xadmin.site.register(Books, BooksAdmin)
# xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
# xadmin.site.register(Banner, BannerGoodsAdmin)
# xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)
#
# xadmin.site.register(HotSearchWords, HotSearchAdmin)
# xadmin.site.register(IndexAd, IndexAdAdmin)

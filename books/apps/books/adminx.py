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
from .models import Books, BooksCategory, BooksImage, BooksBanner


class BooksAdmin(object):
    list_display = ["name", "press", "author",
                    "price", "market_price", "ship_free",
                    "photo", "nums", "revoke", "add_time"]
    search_fields = ['name', ]
    list_filter = ["name", "nums", "add_time"]
    style_fields = {"desc": "ueditor"}


# class BooksImagesInline(object):
# 	model = BooksImage
# 	exclude = ["add_time"]
# 	extra = 1
# 	style = 'tab'

# inlines = [BooksImagesInline]


class BooksCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


# class BooksBrandAdmin(object):
# 	list_display = ["category", "image", "name", "desc"]
#
# 	def get_context(self):
# 		context = super(BooksBrandAdmin, self).get_context()
# 		if 'form' in context:
# 			context['form'].fields['category'].queryset = BooksCategory.objects.filter(category_type=1)
# 		return context
#
#
class BannerBooksAdmin(object):
    list_display = ["user", "books", "image", "index"]


# class HotSearchAdmin(object):
# 	list_display = ["keywords", "index", "add_time"]
#
#
# class IndexAdAdmin(object):
# 	list_display = ["category", "goods"]


xadmin.site.register(Books, BooksAdmin)
xadmin.site.register(BooksCategory, BooksCategoryAdmin)
xadmin.site.register(BooksBanner, BannerBooksAdmin)
# xadmin.site.register(BooksCategoryBrand, BooksBrandAdmin)
#
# xadmin.site.register(HotSearchWords, HotSearchAdmin)
# xadmin.site.register(IndexAd, IndexAdAdmin)

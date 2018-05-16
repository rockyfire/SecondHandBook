# -*- coding: utf-8 -*-
__author__ = 'bobby'

from django.views.generic.base import View

from books.models import Books
# from django.views.generic import ListView


class BooksListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """
        json_list = []
        books = Books.objects.all()[:10]
        # for book in books:
        #     json_dict = {}
        #     json_dict["name"] = book.name
        #     json_dict["category"] = book.category.name
        #     json_dict["market_price"] = book.market_price
        # images field和datetime直接dumps会出错
        #     json_dict["add_time"] = book.add_time
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # for book in books:
        # model_to_dict 将model转换为字典，不用一个字段一个字段提取。
        #     json_dict = model_to_dict(book)
        #
        #     json_list.append(json_dict)

        import json
        from django.core import serializers
        json_data = serializers.serialize('json', books)
        json_data = json.loads(json_data)
        from django.http import HttpResponse, JsonResponse
        return JsonResponse(json_data, safe=False)




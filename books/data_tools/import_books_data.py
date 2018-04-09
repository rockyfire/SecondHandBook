# -*- coding: utf-8 -*-
__author__ = 'bobby'
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Book.settings")

import django

django.setup()

from books.models import Books, BooksImage, BooksCategory,BooksStatus
from data_tools.data.product_data import row_data
from django.contrib.auth import get_user_model

User = get_user_model()

for books_detail in row_data:
    books = Books()
    books.name = books_detail["name"]
    books.press = books_detail["press"]
    books.version = books_detail["version"]

    books.price = float(int(books_detail["price"].replace("￥", "")))
    books.buyoutprice = float(int(books_detail["buyoutprice"].replace("￥", "")))

    books.ship_free = books_detail['ship_free']
    books.desc = books_detail["desc"] if books_detail["desc"] is not None else ""
    books.photo = books_detail["photo"][0] if books_detail["photo"] else ""

    books.nums = int(books_detail['nums'])
    books.status = BooksStatus.objects.filter(name=books_detail['status'])[0]

    category_name = books_detail["categorys"][-1]
    category = BooksCategory.objects.filter(name=category_name)
    if category:
        books.category = category[0]
    user = User.objects.filter(username=books_detail['username'])
    if user:
        books.user = user[0]

    books.save()

    for books_image in books_detail["photo"]:
        books_image_instance = BooksImage()
        books_image_instance.image = books_image
        books_image_instance.books = books
        books_image_instance.save()

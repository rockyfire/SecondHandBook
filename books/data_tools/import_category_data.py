# -*- coding: utf-8 -*-
__author__ = 'bobby'

#独立使用django的model
import sys
import os

# 当前文件所在的绝对路径 .../mysite/db_tools
pwd = os.path.dirname(os.path.realpath(__file__))
# 返回上一层目录 .../mysite
sys.path.append(pwd+"../")
# 需要使用settings中的参数
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Book.settings")

import django
django.setup()

from books.models import BooksCategory

from data_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_intance = BooksCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    # 保存到数据库是CATEGORY_TYPE = ((1, "一级类目"),(2, "二级类目"),(3, "三级类目"),)
    lev1_intance.category_type = 1
    lev1_intance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = BooksCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = BooksCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()


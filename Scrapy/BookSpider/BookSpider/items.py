# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import random


class BookCategoryspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 书籍分类名称
    code = scrapy.Field()  # 书籍分类代码
    desc = scrapy.Field()  # 书籍分类描述

    category_type = scrapy.Field()  # 书籍分类类型
    is_tab = scrapy.Field()  # 书籍分类导航栏显示
    parent_category_id = scrapy.Field()  # 书籍分类父类ID

    def get_insert_sql(self):
        insert_sql = """
                insert into books_bookscategory(
                `name`,code,`desc`,category_type,is_tab,add_time,parent_category_id
                )
                VALUES(%s,%s,%s,%s,%s,%s,%s)
                """
        params = (self['name'], self['code'],
                  self['desc'], self['category_type'],
                  self['is_tab'], datetime.datetime.now(),
                  self['parent_category_id'])
        return insert_sql, params


class BookspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field()
    book_url = scrapy.Field()  # 书籍URL
    book_url_object_id = scrapy.Field()  # 书籍URL  MD5编码

    book_author = scrapy.Field()  # 书籍作者
    book_press = scrapy.Field()  # 书籍出版社
    book_market_price = scrapy.Field()  # 价格
    book_desc = scrapy.Field()  # 简介
    book_short_comment = scrapy.Field()  # 短评
    book_comment = scrapy.Field()  # 书评

    book_image_url = scrapy.Field()  # 书籍图片URL
    book_image_path = scrapy.Field()  # 书籍图片路径

    def get_insert_sql(self):
        insert_sql = """
                    insert into books(
                      book_name,book_url,
                      book_url_object_id,book_author,
                      book_press,book_market_price,
                      book_desc,book_short_comment,
                      book_comment,book_image_url,
                      book_image_path
                    )
                    VALUES(%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s
                    )
                """
        params = (self['book_name'], self['book_url'],
                  self['book_url_object_id'], self['book_author'],
                  self['book_press'], self['book_market_price'],
                  self['book_desc'], self['book_short_comment'],
                  self['book_comment'], self['book_image_url'],
                  self['book_image_path'])
        return insert_sql, params


class BookSellspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    author = scrapy.Field()  # 书籍作者
    press = scrapy.Field()  # 书籍出版社

    market_price = scrapy.Field()  # 参考价格
    desc = scrapy.Field()  # 简介
    photo = scrapy.Field()  # 书籍图片
    category_id = scrapy.Field()  # 书籍分类ID

    book_image_url = scrapy.Field()  # 书籍图片URL

    def get_insert_sql(self):
        insert_sql = """
            insert into books_books(
              `name`,press,author,
              price,market_price,ship_free,
              is_new,photo,`desc`,
              nums,`revoke`,add_time,
              click_num,fav_num,category_id,
              status_id,user_id
            )
            VALUES(
            %s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s
            )
        """
        params = (
            self['name'], self['press'], self['author'],
            float(self['market_price']) - random.randint(0, 9), self['market_price'], 0,
            0, self['photo'], self['desc'],
            random.randint(10, 99), datetime.datetime.now() + datetime.timedelta(days=7), datetime.datetime.now(),
            random.randint(10, 99), random.randint(10, 99), self['category_id'],
            random.choice([1, 2]), 1
        )
        return insert_sql, params

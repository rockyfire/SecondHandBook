# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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
        params=(self['book_name'], self['book_url'],
                self['book_url_object_id'], self['book_author'],
                self['book_press'], self['book_market_price'],
                self['book_desc'], self['book_short_comment'],
                self['book_comment'], self['book_image_url'],
                self['book_image_path'])
        return insert_sql,params


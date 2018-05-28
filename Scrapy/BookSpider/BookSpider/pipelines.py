# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookspiderPipeline(object):
    def process_item(self, item, spider):
        return item


from scrapy.pipelines.images import ImagesPipeline


class BooksImagePipeline(ImagesPipeline):
    # 重写该方法可从result中获取到图片的实际下载地址
    def item_completed(self, results, item, info):
        if "book_image_url" in item:
            for ok, value in results:
                image_file_path = value['path']

        # item["book_image_path"] = image_file_path
        item["photo"] = image_file_path
        return item


import codecs
import json


class JsonWithEncodingPipeline(object):
    """自定义json文件的导出"""

    def __init__(self):
        # codecs 文件编码
        self.file = codecs.open("article.json", 'w', encoding="utf-8")

    def process_item(self, item, spider):
        # 将item转换为dict，然后生成json对象 ensure_ascii=False 防止以unicode编码形式写入文件
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


from scrapy.exporters import JsonItemExporter

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import settings


class MysqlPipeline(object):
    """采用同步的机制写入MySQL"""

    def __init__(self):
        self.conn = MySQLdb.connect(

            "localhost", 'root', '1575', 'books',
            charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql, param = item.get_insert_sql()
        self.cursor.execute(insert_sql, param)
        self.conn.commit()


class MysqlTwistedPipelines(object):
    """采用异步的机制写入MySQL"""

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool=dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, param = item.get_insert_sql()
        cursor.execute(insert_sql, param)


"""
可选django.items
"""

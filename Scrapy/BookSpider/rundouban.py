# -*- coding: utf-8 -*-
# @Author  : Rockyfire
# @Time    : 2018/5/17 9:36


import sys
import os

from scrapy.cmdline import execute

runserver_project_config = "douban"
# 将系统当前目录设置为项目根目录
# os.path.abspath(__file__)为当前文件所在绝对路径
# os.path.dirname为文件所在目录
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
execute(["scrapy", "crawl", runserver_project_config])

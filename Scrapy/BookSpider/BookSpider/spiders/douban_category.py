# -*- coding: utf-8 -*-
import scrapy
from BookSpider.items import BookCategoryspiderItem

from scrapy.http import Request
from urllib import parse
from util import url_md5
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from os import remove

try:
    from PIL import Image
except:
    pass
class DoubanCategorySpider(scrapy.Spider):
    name = 'douban_category'
    allowed_domains = ['www.douban.com']
    # 全部分类
    # start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']
    start_urls = ['https://book.douban.com']

    login_url = "https://www.douban.com/accounts/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    datas = {
        'source': 'index_nav',
        'remember': 'on'
    }
    # 登陆豆瓣
    # def start_requests(self):
    #     return [scrapy.FormRequest(self.login_url,
    #                                headers=self.headers,
    #                                meta={"cookiejar": 1},
    #                                callback=self.login)]

    def login(self, response):
        print("登录前表单填充")
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
        captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()

        if captcha_id is None:
            print('无验证码')

            username = input('请输入账号：')
            password = input('请输入密码：')

            self.datas.update({
                'form_email': username,
                "form_password": password
            })

        else:
            print('有验证码')

            captcha, captcha_id = self.get_captcha()
            self.datas.update({
                'captcha-solution': captcha,
                'captcha-id': captcha_id,
            })

            username = input('请输入账号：')
            password = input('请输入密码：')

            self.datas.update({
                'form_email': username,
                "form_password": password
            })
        print("登录中")
        return scrapy.FormRequest(self.login_url,
                                  meta={'cookiejar': response.meta.get('cookiejar')},
                                  headers=self.headers,
                                  formdata=self.datas,
                                  callback=self.parse_after_login)

    def parse_after_login(self, response):
        '''
        验证登录是否成功
        '''
        account = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
        if account is None:
            print("登录失败")
        else:
            print(u"登录成功,当前账户为 %s" % account)
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    def get_captcha(self):
        r = requests.post(self.login_url, data=self.datas, headers=self.headers)
        page = r.text
        soup = BeautifulSoup(page, "html.parser")
        # 利用bs4获得验证码图片地址
        img_src = soup.find('img', {'id': 'captcha_image'}).get('src')
        urlretrieve(img_src, 'captcha.jpg')
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print('到本地目录打开captcha.jpg获取验证码')
        finally:
            captcha = input('请输入验证码:')
            remove('captcha.jpg')
        captcha_id = soup.find(
            'input', {'type': 'hidden', 'name': 'captcha-id'}).get('value')
        return captcha, captcha_id

    def parse(self, response):
        """
        全部分类
        :param response:
        :return:
        """
        # 全部分类
        # categorys = response.xpath('//*[@id="content"]/div/div[1]/div[2]/div')

        categorys = response.xpath('//*[@id="content"]/div/div[2]/ul/li')
        parent_category_id = 1
        books_category_item = BookCategoryspiderItem()
        for category in categorys:
            # 全部分类
            # category_top_name = category.xpath('a/@name').extract_first("")

            category_top_name = category.xpath('ul/li[1]/text()').extract_first("").replace('\n', '').strip()
            books_category_item['name'] = category_top_name
            books_category_item['code'] = ''
            books_category_item['desc'] = ''
            books_category_item['category_type'] = 1
            books_category_item['is_tab'] = 0
            books_category_item['parent_category_id'] = None

            yield books_category_item
            var_parent_category_id = parent_category_id
            # 全部分类
            # for tr in category.xpath('table/tbody/tr'):
            #     for td in tr.xpath('td'):
            #         category_sec_name = td.xpath('a/text()').extract_first("")
            #         books_category_item['name'] = category_sec_name
            #         books_category_item['code'] = ''
            #         books_category_item['desc'] = ''
            #         books_category_item['category_type'] = 2
            #         books_category_item['is_tab'] = 0
            #         books_category_item['parent_category_id'] = parent_category_id
            #         var_parent_category_id += 1
            #         yield books_category_item

            for tr in category.xpath('ul/li/a'):
                category_sec_name = tr.xpath('text()').extract_first("")
                if '更多' not in category_sec_name:
                    books_category_item['name'] = category_sec_name
                    books_category_item['code'] = ''
                    books_category_item['desc'] = ''
                    books_category_item['category_type'] = 2
                    books_category_item['is_tab'] = 0
                    books_category_item['parent_category_id'] = parent_category_id
                    var_parent_category_id += 1
                    yield books_category_item

            parent_category_id = var_parent_category_id + 1

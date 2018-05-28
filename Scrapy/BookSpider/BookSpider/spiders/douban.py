# -*- coding: utf-8 -*-
import scrapy
import re
from BookSpider.items import BookspiderItem, BookSellspiderItem
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


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']

    # 全部分类
    # start_urls = ['https://book.douban.com/tag/']
    # 部分分类
    start_urls = ['https://book.douban.com']

    login_url = "https://www.douban.com/accounts/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
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
        # 全部分类
        # categorys = response.xpath('//*[@id="content"]/div/div[1]/div[2]/div/table/tbody')

        categorys = response.xpath('//*[@id="content"]/div/div[2]/ul/li')
        # category_id = 1
        for tbody in categorys:
            # 全部分类
            # for tr in tbody.xpath('tr/td'):
            for tr in tbody.xpath('ul/li'):
                post_url = tr.xpath('a/@href').extract_first("")
                # category_id += 1
                yield Request(url=parse.urljoin(response.url, post_url),
                              # meta={'category_id': category_id},
                              callback=self.parse_category)
            # category_id += 1

    # 某一分类下的书籍列表
    def parse_category(self, response):
        category_name = response.xpath('//*[@id="content"]/h1/text()').extract_first("").split(':')[1].strip()
        post_nodes = response.css('ul.subject-list li.subject-item div.info h2 a')

        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={'category_name': category_name},
                          callback=self.parse_detail)

    # 书籍详细信息
    def parse_detail(self, response):

        book_item = BookspiderItem()
        book = BookSellspiderItem()

        category_name = response.meta.get('category_name', '')
        book_url = response.url

        """
        Xpath
        """

        book_name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract_first()
        book_author = response.xpath('//*[@id="info"]/a[1]/text()').extract_first("").replace('\n', '').strip()
        if book_author is None:
            book_author = response.xpath('//*[@id="info"]/span[1]/a/text()').extract_first("").replace('\n', '').strip()

        book_info = response.xpath('//*[@id="info"]/text()').extract()

        # book_market_price = '66.66'
        for select_ele in book_info:
            match_info = select_ele
            # book_market_price = re.search('(\d{1,}\.\d{2})元*', match_info).group(1)
            if '.' in match_info:
                match_info = match_info.strip().replace('元', '').strip()
                book_market_price = match_info
            if '出版' in match_info or '社' in match_info:
                book_press = match_info

        book_desc = response.xpath('string(//div[@class="intro"])').extract()
        book_short_comment = response.xpath('//*[@id="comments"]/ul/li[1]/div/p/text()').extract_first("")
        book_comment = response.xpath('string(//div[@class="short-content"])').extract_first("").strip().replace(' ',
                                                                                                                 '')
        book_image_url = response.xpath('//*[@id="mainpic"]/a/img/@src').extract_first("")

        # comment_list = response.xpath('//*[@id="comments"]/ul/li[2]/div/p')
        # for comment in comment_list:
        #     comment_p=comment.xpath('text()').extract_first()
        #     yield

        """
        CSS
        """
        
        book_item['book_name'] = book_name
        book_item['book_url'] = book_url
        book_item['book_author'] = book_author
        # book_item['book_press'] = book_press
        # book_item['book_market_price'] = book_market_price
        book_item['book_desc'] = book_desc
        book_item['book_short_comment'] = book_short_comment
        book_item['book_comment'] = book_comment
        book_item['book_image_url'] = [book_image_url]  # book_image_url必须是一个数组(List)
        book_item['book_url_object_id'] = url_md5.get_md5(book_image_url)
        # book_item['book_image_path'] = book_image_path

        book['name'] = book_name
        book['author'] = book_author
        book['press'] = book_press
        book['market_price'] = book_market_price
        book['desc'] = book_desc
        book['book_image_url'] = [book_image_url]  # book_image_url必须是一个数组(List)
        book['category_id'] = category_name


        """
        通过ItemLoader加载Item
        """
        print(str(category_name) + book_name)
        # yield book_item
        yield book

# -*- coding: utf-8 -*-
import scrapy
import re
from BookSpider.items import BookspiderItem
from scrapy.http import Request
from urllib import parse


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4']

    def parse(self, response):
        # post_urls = response.xpath('//*[@id="subject_list"]/ul/li[1]/div[2]/h2/a/@href').extract_first()
        post_nodes = response.css('ul.subject-list li.subject-item div.info h2 a')

        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

    def parse_detail(self, response):

        book_url = response.url

        # Xpath
        book_name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract_first()
        book_author = response.xpath('//*[@id="info"]/a[1]/text()').extract_first().replace('\n', '').strip().replace(
            ' ', '')
        book_info = response.xpath('//*[@id="info"]/text()')
        # book_market_price = '66.66'
        for select_ele in book_info:
            match_info = select_ele.extract()
            # book_market_price = re.search('(\d{1,}\.\d{2})元*', match_info).group(1)
            if '.' in match_info:
                match_info = match_info.strip().replace('元', '').strip()
                book_market_price = match_info
            if '出版' in match_info:
                book_press = match_info
        book_desc = response.xpath('string(//div[@class="intro"])').extract()
        book_short_comment = response.xpath('//*[@id="comments"]/ul/li[1]/div/p/text()').extract_first("")
        book_comment = response.xpath('string(//div[@class="short-content"])').extract_first("").strip().replace(' ',
                                                                                                                 '')
        book_image_url = response.xpath('//*[@id="mainpic"]/a/img/@src').extract_first("")
        """
        CSS
        """

        book_item = BookspiderItem()
        book_item['book_name'] = book_name
        book_item['book_url'] = book_url
        book_item['book_author'] = book_author
        book_item['book_press'] = book_press
        book_item['book_market_price'] = book_market_price
        book_item['book_desc'] = book_desc
        book_item['book_short_comment'] = book_short_comment
        book_item['book_comment'] = book_comment
        # book_image_url必须是一个数组(List)
        book_item['book_image_url'] = [book_image_url]

        from util import url_md5
        book_item['book_url_object_id'] = url_md5.get_md5(book_image_url)

        # book_item['book_image_path'] = book_image_path
        
        """
        通过ItemLoader加载Item
        """

        yield book_item

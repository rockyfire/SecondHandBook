#!/usr/bin/env python
# encoding: utf-8

row_data = [
    {
        "username":"rockyfire",
        'name':'三体',
        'press':'重庆出版社',
        'version':'第一版',
        'price': '￥66',
        'buyoutprice': '￥166',
        'ship_free': 'True',
        'photo': [
            'books/images/1_P_1449024889889.jpg',
            'books/images/1_P_1449024889264.jpg',
            'books/images/1_P_1449024889726.jpg',
            'books/images/1_P_1449024889018.jpg',
            'books/images/1_P_1449024889287.jpg'
        ],
        'nums': '100',
        'revoke':'2018-01-01 01:01:01',
        'status':'1',
        'desc':'<p><img src="/media/books/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        "username":"rockyfire",
        'name': '最后一个地球',
        'press': '重庆出版社',
        'version': '第一版',
        'price': '￥66',
        'buyoutprice': '￥166',
        'ship_free': 'True',
        'photo': [
            'books/images/1_P_1449024889889.jpg',
            'books/images/1_P_1449024889264.jpg',
            'books/images/1_P_1449024889726.jpg',
            'books/images/1_P_1449024889018.jpg',
            'books/images/1_P_1449024889287.jpg'
        ],
        'nums': '100',
        'revoke': '2018-01-01 01:01:01',
        'status': '1',
        'desc': '<p><img src="/media/books/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        "username": "rockyfire",
        'name': '星球大战',
        'press': '重庆出版社',
        'version': '第一版',
        'price': '￥66',
        'buyoutprice': '￥166',
        'ship_free': 'True',
        'photo': [
            'books/images/1_P_1449024889889.jpg',
            'books/images/1_P_1449024889264.jpg',
            'books/images/1_P_1449024889726.jpg',
            'books/images/1_P_1449024889018.jpg',
            'books/images/1_P_1449024889287.jpg'
        ],
        'nums': '100',
        'revoke': '2018-01-01 01:01:01',
        'status': '1',
        'desc': '<p><img src="/media/books/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        "username": "rockyfire",
        'name': '太空漫游',
        'press': '重庆出版社',
        'version': '第一版',
        'price': '￥66',
        'buyoutprice': '￥166',
        'ship_free': 'True',
        'photo': [
            'books/images/1_P_1449024889889.jpg',
            'books/images/1_P_1449024889264.jpg',
            'books/images/1_P_1449024889726.jpg',
            'books/images/1_P_1449024889018.jpg',
            'books/images/1_P_1449024889287.jpg'
        ],
        'nums': '100',
        'revoke': '2018-01-01 01:01:01',
        'status': '1',
        'desc': '<p><img src="/media/books/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        "username": "rockyfire",
        'name': '1984',
        'press': '重庆出版社',
        'version': '第一版',
        'price': '￥66',
        'buyoutprice': '￥166',
        'ship_free': 'True',
        'photo': [
            'books/images/1_P_1449024889889.jpg',
            'books/images/1_P_1449024889264.jpg',
            'books/images/1_P_1449024889726.jpg',
            'books/images/1_P_1449024889018.jpg',
            'books/images/1_P_1449024889287.jpg'
        ],
        'nums': '100',
        'revoke': '2018-01-01 01:01:01',
        'status': '1',
        'desc': '<p><img src="/media/books/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        "username": "rockyfire",
        'name':'基地',
        'press':'重庆出版社',
        'version':'第一版',
        'price': '￥66',
        'buyoutprice': '￥166',
        'ship_free': 'True',
        'photo': [
            'books/images/1_P_1449024889889.jpg',
            'books/images/1_P_1449024889264.jpg',
            'books/images/1_P_1449024889726.jpg',
            'books/images/1_P_1449024889018.jpg',
            'books/images/1_P_1449024889287.jpg'
        ],
        'nums': '100',
        'revoke':'2018-01-01 01:01:01',
        'status':'1',
        'desc':'<p><img src="/media/books/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
    {
        "username": "rockyfire",
        'name': '雪地',
        'press': '重庆出版社',
        'version': '第一版',
        'price': '￥66',
        'buyoutprice': '￥166',
        'ship_free': 'True',
        'photo': [
            'books/images/1_P_1449024889889.jpg',
            'books/images/1_P_1449024889264.jpg',
            'books/images/1_P_1449024889726.jpg',
            'books/images/1_P_1449024889018.jpg',
            'books/images/1_P_1449024889287.jpg'
        ],
        'nums': '100',
        'revoke': '2018-01-01 01:01:01',
        'status': '2',
        'desc': '<p><img src="/media/books/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/books/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
]

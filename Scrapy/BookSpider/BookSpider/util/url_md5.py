# -*- coding: utf-8 -*-
# @Author  : Rockyfire
# @Time    : 2018/5/17 14:47

import hashlib


def get_md5(url):
    # python3
    # encode unicode -->str
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# !/usr/bin/env python3
# *coding:utf-8*
__author__ = 'rockyfire'

import requests
import time
import hashlib
import json


class SendMessage(object):

    def __init__(self, accountsid, token):
        self.token = token
        self.accountSid = accountsid
        self.url = "https://api.miaodiyun.com/20150822/industrySMS/sendSMS"
        self.timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    def send_sms(self, code, mobile):
        params = {
            "accountSid": self.accountSid,
            "templateid": "146697495",
            "param": code,
            "to": mobile,
            "timestamp": self.timestamp,
            "sig": hashlib.md5((self.accountSid + self.token + self.timestamp).encode('utf-8')).hexdigest(),
        }
        response = requests.post(self.url, data=params)
        re_dict = json.loads(response.text)

        return re_dict
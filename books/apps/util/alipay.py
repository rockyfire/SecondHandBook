# -*- coding: utf-8 -*-

# pip install pycryptodome
__author__ = 'rockyfire'

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes

import json


class AliPay(object):
    """
    支付宝支付接口
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        # 验证支付宝返回的消息
        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.import_key(fp.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        # 请求的相关参数
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    # 公告请求参数在前 biz_content嵌套关系
    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        # 使用&进行连接
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        # 签名
        sign = self.sign(unsigned_string.encode("utf-8"))
        # ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车 byte - utf8字符串
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    # 验证支付宝返回的结果是否合法
    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    alipay = AliPay(
        appid="2016091300498040",
        # 异步接受支付宝返回的状态，进而修改该订单的状态
        app_notify_url="http://165.227.231.209:8087/alipay/return/",
        app_private_key_path=u"private2048.txt",
        alipay_public_key_path="alipay_key_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False,
        # 支付成功后跳转到商户页面
        return_url="http://165.227.231.209:8087/alipay/return/"
    )

    # 支付宝返回数据验证
    return_url = 'http://165.227.231.209:8087/?total_amount=0.01&timestamp=2018-04-04+10%3A41%3A38&sign=cqc0wvkc%2BeoW276ECB2VuLUE9zNi3wQmVEtzGThCjXv7sHex866hskj9szHxmoegpXGARqlPM9EfM9kbloMFKPyaLY6RvcTZOpJvRNXkW3LVzg7c9z%2FinNKuSeF%2BzEdE04DEkjYp1WNX%2FGcQ7%2FMKooZnV%2F2VS6Y0Mwn%2FFELVocodpIbIE4z3rx0MSzw834AXm1zOT16md4Gh7pzVQCyfYaMcQ209oKqofGd%2FRsWBufN8Uxd0%2Bn4G15e2dRel0ArFPP3yE4azyhz7e9fzYGc2CHTFdpSrYSle3S0%2B2YGW2XESo1KU857fifpNQBWzQZ1jvaO2nHTKkVSVOCReveu3PA%3D%3D&trade_no=2018040421001004060200250636&sign_type=RSA2&auth_app_id=2016091300498040&charset=utf-8&seller_id=2088102175372352&method=alipay.trade.page.pay.return&app_id=2016091300498040&out_trade_no=201702021222&version=1.0'
    o = urlparse(return_url)
    query = parse_qs(o.query)
    processed_query = {}
    ali_sign = query.pop("sign")[0]
    for key, value in query.items():
        processed_query[key] = value[0]
    # print(alipay.verify(processed_query, ali_sign))

    url = alipay.direct_pay(
        subject="测试订单",
        out_trade_no="201702021231",
        total_amount=0.01
    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    print(re_url)

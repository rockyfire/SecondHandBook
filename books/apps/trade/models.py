from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from books.models import Books
from user_operation.models import UserAddress

User = get_user_model()


# Create your models here.


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name=u"用户")
    books = models.ForeignKey(Books, verbose_name=u"书籍")
    nums = models.IntegerField(default=0, verbose_name="购买数量")

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "books")

    def __str__(self):
        return "%s(%d)".format(self.books.name, self.nums)


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("PAYING", "待支付"),
    )

    user = models.ForeignKey(User, verbose_name="用户")
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号")
    trade_no = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name=u"交易号")
    pay_status = models.CharField(choices=ORDER_STATUS, default="PAYING", max_length=30, verbose_name="订单状态")
    post_script = models.CharField(max_length=200, null=True, blank=True, verbose_name="订单留言")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 用户信息
    address = models.ForeignKey(UserAddress, verbose_name="用户地址")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderBooks(models.Model):
    """
    订单的书籍详情
    """
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="books")
    books = models.ForeignKey(Books, verbose_name="书籍")
    books_num = models.IntegerField(default=0, verbose_name="书籍数量")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单书籍"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)

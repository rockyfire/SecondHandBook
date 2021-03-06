from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from util.permissions import IsOwnerOrReadOnly
from rest_framework import serializers
from .models import ShoppingCart, OrderInfo, OrderBooks
from .serializer import ShopCartSerializer, ShopCartDetailSerializer, OrderDetailSerializer, OrderSerializer, \
    SoldBooksSerialzier
from .filters import SoldBooksFilter
from django_filters import rest_framework as djnagofilters
from rest_framework import filters
from books.models import Books



# Create your views here.


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物车
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "books_id"

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    # 细节完善 书籍数量变化
    # 库存变化
    def perform_destroy(self, instance):
        books = instance.books
        books.nums += instance.nums
        books.save()
        instance.delete()

    # 删除购物车中的所有商品
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        books = shop_cart.books
        books.nums -= shop_cart.nums
        books.save()

    # 更新操作
    def perform_update(self, serializer):
        # 获取购物车之前的数据进行对比
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        save_record = serializer.save()

        nums = save_record.nums - existed_nums
        books = save_record.books

        books.nums -= nums
        if books.nums < 0:
            raise serializers.ValidationError("已售空")
        books.save()


class OrderViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    订单管理：
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    # 创建订单时，购物车中的信息保存到订单信息（生成）和订单书籍信息（保存书籍数量）
    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_books = OrderBooks()
            order_books.order = order
            order_books.books = shop_cart.books
            order_books.books_num = shop_cart.nums
            order_books.save()

            # 清空购物车
            shop_cart.delete()
        return order


from rest_framework.views import APIView
from Book.settings import ali_pub_key_path, private_key_path
from util.alipay import AliPay
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import redirect


class AlipayViewSet(APIView):
    def __init__(self):
        self.alipay = AliPay(
            appid="2016091300498040",
            # 异步接受支付宝返回的状态，进而修改该订单的状态
            app_notify_url="http://flycode.me:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用.
            debug=True,  # 默认False,
            # 支付成功后跳转到商户页面
            return_url="http://flycode.me:8000/"
        )

    def get(self, request):
        """
        return_url的操作 notify_url都会修改订单状态。
        :param request:
        :return:
        """
        response = redirect("/index/#/app/home/member/order")
        return response

    def post(self, request):
        """
        notify_url
        :param request: 
        :return: 
        """
        processed_dict = {}

        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        verify_re = self.alipay.verify(processed_dict, sign)

        # 更新操作
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            return Response("success")


class SoldBooksViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = SoldBooksSerialzier

    filter_backends = (djnagofilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = SoldBooksFilter
    ordering_fields = ('add_time',)

    def get_queryset(self):
        # 查询是当前用户出售书籍的订单
        books = Books.objects.filter(user=self.request.user)
        result = OrderBooks.objects.filter(books__in=[i.id for i in books])
        return result

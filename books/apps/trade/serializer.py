from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from .models import ShoppingCart, OrderInfo, OrderBooks
from books.serializers import BooksSerializer, BookCreateSerializer
from books.models import Books
from django.utils import timezone
from util.alipay import AliPay
from Book.settings import ali_pub_key_path, private_key_path
from users.serializer import UserInfoSerializer


class ShopCartDetailSerializer(serializers.ModelSerializer):
    """
        购物车详情
    """
    # 一条购物车关系记录对应的只有一个goods。
    books = BooksSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(
        required=True, label="数量", min_value=1,
        error_messages={
            "min_value": "商品数量必须大于1",
            "required": "必须填写数量"
        }
    )

    books = serializers.PrimaryKeyRelatedField(required=True, queryset=Books.objects.all())

    # validated_data是数据已经经过validate之后的数据。
    # 而initial_data是未经validate处理过的原始值。需要我们自己进行类型转换等。

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        books = validated_data['books']
        existed = ShoppingCart.objects.filter(user=user, books=books)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderBooksSerialzier(serializers.ModelSerializer):
    books = BooksSerializer(many=False)

    class Meta:
        model = OrderBooks
        fields = "__all__"


# 个人中心使用
class OrderDetailSerializer(serializers.ModelSerializer):
    # 外键related_name
    order_books = OrderBooksSerialzier(many=True)
    # 用户详情
    user = UserInfoSerializer()
    # 订单形成但还没支付
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016091300498040",
            # 异步接受支付宝返回的状态，进而修改该订单的状态
            app_notify_url="http://flycode.me:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用.
            debug=True,  # 默认False,
            # 支付成功后跳转到商户页面
            return_url="http://flycode.me:8000/index/#/app/home/member/order"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            # 商户自己平台的订单号
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"
        # or
        # read_only_fields = ('alipay_url',)
        # extra_kwargs = {'alipay_url': {'read_only': True}}


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016091300498040",
            # 异步接受支付宝返回的状态，进而修改该订单的状态
            app_notify_url="http://flycode.me:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用.
            debug=True,  # 默认False,
            # 支付成功后跳转到商户页面
            return_url="http://flycode.me:8000/index/#/app/home/member/order"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    # 部分订单信息不是用户可以提交的值。所以给部分订单信息添加readonly
    pay_status = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)
    add_time = serializers.CharField(read_only=True)

    # 生成订单号 时间戳+用户ID+两位随机数
    def generate_order_sn(self):
        import random
        import time
        order_sn = "{time_str}{userid}{restr}".format(
            time_str=time.strftime("%Y%m%d%H%M%S"),
            userid=self.context['request'].user.id,
            restr=random.randint(10, 99)
        )
        return order_sn

    # 根据mixins.CreateModelMixin和generics.GenericAPIView 可知流程步骤是序列化，验证，保存，返回状态码
    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


from users.serializer import UserDetailSerializer


class SoldOrderSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = OrderInfo
        fields = "__all__"


# 已卖出的宝贝
class SoldBooksSerialzier(serializers.ModelSerializer):
    books = BooksSerializer(many=False)
    order = SoldOrderSerializer(many=False)

    class Meta:
        model = OrderBooks
        fields = "__all__"

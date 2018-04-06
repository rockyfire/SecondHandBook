from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from .models import ShoppingCart, OrderInfo, OrderBooks
from books.serializers import BooksSerializer
from books.models import Books
from django.utils import timezone
from util.alipay import AliPay
from Book.settings import ali_pub_key_path, private_key_path


class ShopCartDetailSerializer(serializers.ModelSerializer):
    books = BooksSerializer(many=False, )

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
    # Model字段books
    books = BooksSerializer(many=False)

    class Meta:
        model = OrderBooks
        fields = "__all__"


# 个人中心使用
class OrderDetailSerializer(serializers.ModelSerializer):
    # 外键related_name
    books = OrderBooksSerialzier(many=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)
    # alipay_url = serializers.SerializerMethodField(editable = False)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016091300498040",
            # 异步接受支付宝返回的状态，进而修改该订单的状态
            app_notify_url="http://165.227.231.209:8087/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用.
            debug=True,  # 默认False,
            # 支付成功后跳转到商户页面
            return_url="http://165.227.231.209:8087/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"
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
            app_notify_url="http://165.227.231.209:8087/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用.
            debug=True,  # 默认False,
            # 支付成功后跳转到商户页面
            return_url="http://165.227.231.209:8087/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    pay_status = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

    add_time = serializers.HiddenField(
        default=timezone.now
    )

    def generate_order_sn(self):
        import random
        import time
        order_sn = "{time_str}{userid}{restr}".format(
            time_str=time.strftime("%Y%m%d%H%M%S"),
            userid=self.context['request'].user.id,
            restr=random.randint(10, 99)
        )
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"

from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from .models import ShoppingCart, OrderInfo, OrderBooks
from books.serializers import BooksSerializer
from books.models import Books
from django.utils import timezone


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

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

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

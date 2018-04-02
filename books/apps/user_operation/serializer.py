from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from .models import UserFav, UserLeavingMessage, UserAddress
from books.serializers import BooksSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    books = BooksSerializer

    class Meta:
        model = UserFav
        fields = ('books', "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ("user", "books", "id")
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'books'),
                message="已经收藏"
            )
        ]


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message')


from django.utils import timezone


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.HiddenField(
        default=timezone.now
    )

    class Meta:
        model = UserAddress
        fields = '__all__'

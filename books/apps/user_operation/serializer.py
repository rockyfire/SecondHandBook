from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from .models import UserFav
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

from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from .models import Comment
from books.serializers import BooksSerializer


# class CurrentBooksDefault(object):
#     def set_context(self, serializer_field):
#         self.books = serializer_field.context['request'].books
#
#     def __call__(self):
#         return self.books


class UserCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # books = serializers.HiddenField(
    #     default=serializers.CurrentBooksDefault()
    # )
    books = BooksSerializer

    class Meta:
        model = Comment
        fields = '__all__'


class BookCommentSerializer(serializers.ModelSerializer):
    books = BooksSerializer

    class Meta:
        model = Comment
        fields = '__all__'

from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from .models import Comment


class CurrentBooksDefault(object):
    def set_context(self, serializer_field):
        self.books = serializer_field.context['request'].books

    def __call__(self):
        return self.books


class UserCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    content = serializers.CharField(
        required=True,
        error_messages={
            'required': '必须填写评论'
        }
    )

    def create(self, validated_data):
        existed = Comment.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改评论
        instance.content = validated_data['content']
        instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ("user", "content", "books", "id",)


class BookCommentSerializer(serializers.ModelSerializer):
    # books = BooksSerializer(many=False)

    class Meta:
        model = Comment
        fields = '__all__'

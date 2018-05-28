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


from .models import Reply


class ReplyCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('content_type', 'object_pk',
                  'site', 'comment', 'submit_date',
                  'ip_address', 'parent',
                  )
        extra_kwargs = {
            'submit_date': {'required': False, 'allow_null': True},

            # 似乎以下设置没有生效
            'ip_address': {'required': False, 'allow_null': True},
            'site': {'default': 1},
        }


from .models import BooksComment
from django.contrib.contenttypes.models import ContentType
from books.models import Books
from users.serializer import UserInfoSerializer


class BooksCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        validated_data['content_type'] = ContentType.objects.get_for_model(Books)
        existed = BooksComment.objects.create(**validated_data)
        return existed

    class Meta:
        model = BooksComment
        fields = ('text', 'object_id','user')


# 评论详情
class BooksCommentDetailSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()

    class Meta:
        model = BooksComment
        fields = '__all__'

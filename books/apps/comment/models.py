from datetime import datetime

from django.db import models

from books.models import Books
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    books = models.ForeignKey(Books, verbose_name="书籍", related_name="r_comments")
    point = models.IntegerField(default=10, verbose_name="书籍打分")
    content = models.TextField(max_length=140, verbose_name="评论内容", help_text="评论内容")
    reply = models.CharField(max_length=32, verbose_name="回复内容")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class BooksComment(models.Model):
    """
    书籍的评论详情
    """
    book = models.ForeignKey(Books, verbose_name="书籍", related_name="BooksComment_comments")
    comments = models.ForeignKey(Comment, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "书籍评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.books.id)


from django_comments.abstracts import CommentAbstractModel
from mptt.models import MPTTModel, TreeForeignKey


class Reply(MPTTModel, CommentAbstractModel):
    parent = TreeForeignKey('self', null=True, blank=True,
                            verbose_name='上级回复', related_name='children',
                            on_delete=models.SET_NULL
                            )

    class Meta(CommentAbstractModel.Meta):
        verbose_name = '回复'
        verbose_name_plural = verbose_name

    def descendants(self):
        """
        获取回复的全部子孙回复，按回复时间正序排序
        """
        return self.get_descendants().order_by('submit_date')

# 自己实现评论功能

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class MyComment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=u"用户",on_delete=models.DO_NOTHING)
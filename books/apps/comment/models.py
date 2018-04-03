from datetime import datetime

from django.db import models

from books.models import Books
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    books = models.ForeignKey(Books, verbose_name="书籍", related_name="comments")
    point = models.IntegerField(default=10, verbose_name="书籍打分")
    content = models.TextField(max_length=140, verbose_name="评论内容", help_text="评论内容")
    reply = models.CharField(max_length=32, verbose_name="回复内容")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name


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

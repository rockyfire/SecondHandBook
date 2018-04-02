from datetime import datetime

from django.db import models

from books.models import Books
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    books = models.ForeignKey(Books, verbose_name="书籍")
    point = models.IntegerField(default=10, verbose_name="书籍打分")
    content = models.TextField(max_length=140, verbose_name="评论内容", help_text="评论内容")
    reply = models.CharField(max_length=32, verbose_name="回复内容")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name
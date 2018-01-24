from datetime import datetime

from django.db import models

from books.models import Books


# Create your models here.

class Comment(models.Model):
    books = models.ForeignKey(Books, verbose_name="书籍")
    point = models.IntegerField(default=10, verbose_name="书籍打分")
    content = models.TextField(max_length=140, verbose_name="评论内容", help_text="评论内容")
    reply = models.CharField(max_length=32, verbose_name="回复内容")

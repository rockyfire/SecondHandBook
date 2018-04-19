# _*_ coding:utf-8 _*_
__author__ = 'rockyfire'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        books = instance.books
        books.fav_num += 1
        books.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    books = instance.books
    books.fav_num -= 1
    books.save()

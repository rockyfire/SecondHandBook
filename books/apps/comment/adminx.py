# -*- coding: utf-8 -*-
__author__ = 'bobby'

import xadmin
from .models import Comment


class CommentAdmin(object):
    list_display = ["books", "point", "content", "reply"]


xadmin.site.register(Comment, CommentAdmin)

from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Comment
from .serializer import UserCommentSerializer, BookCommentSerializer, ReplyCreationSerializer


# Create your views here.


class BooksCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # def get_queryset(self):
    #     return Comment.objects.filter(books=self.request.books)

    def get_serializer_class(self):
        if self.action == "list":
            return BookCommentSerializer
        elif self.action == "create":
            return UserCommentSerializer
        return UserCommentSerializer


from rest_framework.generics import (
    CreateAPIView,
)
from django_comments import signals
from rest_framework import permissions


# from .serializers import ReplyCreationSerializer


class ReplyCreationViewSet(CreateAPIView):
    serializer_class = ReplyCreationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        parent_reply = serializer.validated_data.get('parent')
        reply = serializer.save(user=self.request.user, parent=parent_reply)
        signals.comment_was_posted.send(
            sender=reply.__class__,
            comment=reply,
            request=self.request
        )


from .serializer import BooksCommentSerializer
from .models import BooksComment


class MyCommentViewSet(viewsets.ModelViewSet):
    serializer_class = BooksCommentSerializer
    queryset = BooksComment.objects.all()

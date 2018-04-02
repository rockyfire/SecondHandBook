from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Comment
from .serializer import UserCommentSerializer, BookCommentSerializer


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

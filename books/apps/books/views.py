from django.shortcuts import render
from .models import Books, BooksCategory
from .serializers import BooksSerializer, CategorySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# Create your views here.

# Django restful framework
# Create your views here.
# class BooksListView(APIView):
# 	"""
# 		Books All List
# 	"""
#
# 	def get(self, request, ):
# 		books = Books.objects.all()[:10]
# 		# 多个对象，所以要配置many=True
# 		books_serializer = BooksSerializer(books, many=True)
# 		return Response(books_serializer.data)
#
# 	def post(self, request, format=None):
# 		serializer = BooksSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    # 一页显示的个数
    page_size_query_param = 'page_size'
    # 自定义请求参数 默认是page=
    page_query_param = "p"
    max_page_size = 3
    last_page_strings = ('最后一页',)


from rest_framework import mixins, viewsets
from .filters import BooksFilter
from django_filters import rest_framework as djnagofilters
from rest_framework import filters


# class BooksListView(generics.ListAPIView):
class BooksListView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        Goods All List Mixins
    """
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    # pagination_class = LargeResultsSetPagination

    filter_backends = (djnagofilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BooksFilter
    search_fields = ('=name',)
    ordering_fields = ('price',)


class BooksCategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        商品分类列表数据
    """
    # queryset = BooksCategory.objects.all()
    # 获取分类为一的数据 一级分类
    queryset = BooksCategory.objects.filter(category_type=1)

    serializer_class = CategorySerializer

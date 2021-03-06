from django.shortcuts import render
from .models import Books, BooksCategory, BooksImage, BooksBanner, BooksStatus
from .serializers import BooksSerializer, CategorySerializer, CategorySerializer2, BookCreateSerializer, \
    BookBannerSerializer, \
    IndexStatusSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from .filters import BooksFilter
from django_filters import rest_framework as djnagofilters
from rest_framework import filters
from django.db.models import Q

from users.models import UserProfile
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


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 4
    # 一页显示的个数
    page_size_query_param = 'page_size'
    # 自定义请求参数 默认是page=
    page_query_param = "page"
    max_page_size = 10
    last_page_strings = ('最后一页',)


# class BooksListView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
class BooksListView(viewsets.ReadOnlyModelViewSet):
    """
        Goods All List Mixins
    """
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    pagination_class = LargeResultsSetPagination

    filter_backends = (djnagofilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BooksFilter
    search_fields = ('=name',)
    ordering_fields = ('price', 'add_time', 'click_num', 'fav_num')

    # 过滤
    # def get_queryset(self):
    #     price_min = self.request.query_params.get('price')
    #     if price_min:
    #         self.queryset=Books.objects.filter(shop_price__gt=price_min)
    #     return self.queryset

    # 扩展功能
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.click_nums += 1
    #     instance.save()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)


class BooksCreateView(viewsets.ModelViewSet):
    """
        由用户创建的书籍
    """
    serializer_class = BookCreateSerializer
    pagination_class = LargeResultsSetPagination

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Books.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        books = serializer.save()
        booksImage = BooksImage.objects.create(books=books, image=books.photo)
        booksImage.save()


class BooksCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List:
        书籍分类列表数据
    """

    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategorySerializer2
        return CategorySerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return BooksCategory.objects.filter(Q(category_type=1) | Q(category_type=2))
        return BooksCategory.objects.filter(Q(category_type=1))


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        管理员有添加书籍轮播图的权限，
    """
    queryset = BooksBanner.objects.all().order_by('add_time')
    serializer_class = BookBannerSerializer


class IndexStatusViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        书籍所属的模块 书籍状态
    """
    queryset = BooksStatus.objects.filter(name__in=["书城", "征书墙"])
    serializer_class = IndexStatusSerializer

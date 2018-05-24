"""Book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls

from Book.settings import MEDIA_ROOT
from django.views.static import serve
from django.views.decorators.csrf import csrf_exempt

from users.views import SmsCodeViewset, UserViewset
from books.views import BooksListView, BooksCategoryViewSet, BooksCreateView, BannerViewset, IndexStatusViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from trade.views import ShoppingCartViewset, OrderViewset,SoldBooksViewSet
from comment.views import BooksCommentViewSet
import xadmin


router = DefaultRouter()
# router.register(r'users',UserViewSet,base_name="users")
router.register(r'sendmessage', SmsCodeViewset, base_name="sendmessage")
# 用户注册，用户详细信息
router.register(r'users', UserViewset, base_name='users')
# 书籍管理
router.register(r'books', BooksListView, base_name='books')
router.register(r'bookscreate', BooksCreateView, base_name='bookscreate')
# 首页模块功能
router.register(r'indexmodule', IndexStatusViewSet, base_name='indexmodule')


# 书籍分类管理
router.register(r'bookscategory', BooksCategoryViewSet, base_name='bookscategory')
# 用户操作管理
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
router.register(r'userleavingmessage', UserLeavingMessageViewSet, base_name='userleavingmessage')
router.register(r'useraddress', UserAddressViewSet, base_name='useraddress')
# 评论管理
router.register(r'comment', BooksCommentViewSet, base_name="comment")
# 交易管理
router.register(r'shoppingcart', ShoppingCartViewset, base_name="shoppingcart")
router.register(r'order', OrderViewset, base_name="order")
router.register(r'sold', SoldBooksViewSet, base_name="sold")
# 轮播图
router.register(r'banner', BannerViewset, base_name="banner")

from trade.views import AlipayViewSet
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^', include(router.urls)),
    # url(r'^books',BooksListView.as_view(),name='books'),

    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Django Rest Framework 自带的Token认证模式
    url(r'^api-token-auth/',  views.obtain_auth_token),
    # Json Web Token的认证接口
    url(r'^login/', obtain_jwt_token),
    # 自动化文档,1.11版本中注意此处前往不要加$符号
    url(r'docs/', include_docs_urls(title="袋鼠二手书交易系统")),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^alipay/return/', AlipayViewSet.as_view(), name='alipay'),

    url(r'^index', TemplateView.as_view(template_name="index.html"), name='index'),

    url(r'^ueditor',include('DjangoUeditor.urls'),name='ueditor'),
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT})


    # 聊天室
    url(r'^chat/', include('chat.urls')),
]

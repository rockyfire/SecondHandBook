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

from users.views import SmsCodeViewset, UserViewset
import xadmin

router = DefaultRouter()
# router.register(r'users',UserViewSet,base_name="users")
router.register(r'sendmessage', SmsCodeViewset, base_name="sendmessage")
# 用户注册，用户详细信息
router.register(r'users', UserViewset, base_name='users')

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^xadmin/',xadmin.site.urls),
	url(r'^', include(router.urls)),

	url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

	# Django Rest Framework 自带的Token认证模式
	url(r'^api-token-auth/', views.obtain_auth_token),
	# Json Web Token的认证接口
	url(r'^login/', obtain_jwt_token),
	url(r'docs/', include_docs_urls(title="二手书交易平台")),

	url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
]

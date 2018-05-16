from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    只有所有者才可以做修改，其他人只能只读
    has_object_permission，是否有对象权限


    auth是用来做用户验证的，permission是用来做权限判断的。

    AllowAny:不管有没有权限都可以访问。

    IsAuthenticated: 判断是否已经登录

    IsAdminUser：判断用户是否是一个管理员。Model中user.is_staff

    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # 会检测我们从数据库中拿出来的obj的user是否等于request.user
        return obj.user == request.user

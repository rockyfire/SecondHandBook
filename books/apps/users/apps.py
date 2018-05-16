from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户"

    # 这是AppConfig中我们可以在子类中自定义的函数，它将会在django启动时被运行。
    def ready(self):
        import users.signals

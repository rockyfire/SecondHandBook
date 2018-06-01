import datetime

from django.db import models

from DjangoUeditor.models import UEditorField
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import BooksComment
from django.contrib.auth import get_user_model

User = get_user_model()


class BooksCategory(models.Model):
    """
    书籍类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
    )
    id = models.AutoField(primary_key=True, verbose_name="类别ID", help_text="类别ID")
    name = models.CharField(unique=True, max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    # 设置目录树的级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    # 自关联
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "书籍类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BooksCategoryBrand(models.Model):
    """
    某一大类下的宣传商标
    """
    category = models.ForeignKey(BooksCategory, related_name='brands', null=True, blank=True, verbose_name="书籍类目")
    name = models.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = models.TextField(default="", max_length=200, verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "宣传品牌"
        verbose_name_plural = verbose_name
        db_table = "bookscategory_brand"

    def __str__(self):
        return self.name


class BooksStatus(models.Model):
    """
    书籍状态：比如书城，征书墙等
    """
    name = models.CharField(max_length=100, verbose_name="名字")

    class Meta:
        verbose_name = '书籍状态'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Books(models.Model):
    """
    书籍详情表
    """
    user = models.ForeignKey(User, verbose_name="用户")
    category = models.ForeignKey(BooksCategory, verbose_name='书籍类目', to_field="name", related_name='category_books')
    status = models.ForeignKey(BooksStatus, verbose_name="书籍状态")

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="书籍名称")
    press = models.CharField(max_length=100, null=True, blank=True, verbose_name="出版社")
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name="书籍作者")

    price = models.FloatField(default=0, verbose_name="书籍价格")
    market_price = models.FloatField(default=0, verbose_name="参考价格")

    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    is_new = models.BooleanField(default=False, verbose_name="最新上架")

    photo = models.FileField(upload_to="books/images/", null=True, blank=True, verbose_name="书籍图片")
    desc = UEditorField(imagePath="books/images/", width=1024, height=300,
                        filePath="books/files/", default='', verbose_name=u"书籍描述信息", )
    nums = models.IntegerField(default=0, verbose_name="书籍数量")
    revoke = models.DateField(default=datetime.datetime.now() + datetime.timedelta(days=7), verbose_name="下架时间")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    # 未实现的功能
    # views_num = models.PositiveIntegerField(default=0)
    # from django.contrib.contenttypes.fields import GenericRelation
    # from comment.models import Reply
    # replies = GenericRelation(Reply,object_id_field='object_pk',
    #                           content_type_field='content_type',verbose_name="回复")

    # 扩展功能
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")

    books_comment = GenericRelation(BooksComment, related_query_name='books_comments')

    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    # def increase_views_num(self):
    #     self.views_num += 1
    #     self.save(update_fields=['views_num'])

    def __str__(self):
        return self.name


class BooksImage(models.Model):
    """
    书籍轮播图 使用在书籍详情中
    """
    books = models.ForeignKey(Books, verbose_name="书籍", related_name="images")
    image = models.ImageField(upload_to="books/images/", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '书籍图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.books.name


class BooksBanner(models.Model):
    """
    轮播的书籍 首页轮播的商品图，为适配首页大图
    """
    user = models.ForeignKey(User, verbose_name="用户")
    books = models.ForeignKey(Books, verbose_name="书籍")
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播书籍'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'books')

    def __str__(self):
        return self.books.name


class HotSearchWords(models.Model):
    """
    热搜榜
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords

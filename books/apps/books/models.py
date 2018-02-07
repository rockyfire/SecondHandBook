import datetime

from django.db import models

from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model

User = get_user_model()


class BooksCategory(models.Model):
	"""
	书籍类别
	"""
	CATEGORY_TYPE = (
		(1, "一级类目"),
		(2, "二级类目"),
		(3, "三级类目"),
	)

	name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
	code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
	desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
	category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
	parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
										related_name="sub_cat")
	is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
	add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "书籍类别"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


# Create your models here.

class Books(models.Model):
	"""
	书籍
	"""
	STATUS_CHOICES = (
		(1, "书城"),
		(2, "征书墙"),
		(3, "竞拍"),
		(4, "下架"),
	)
	user = models.ForeignKey(User, verbose_name="用户")
	category = models.ForeignKey(BooksCategory, verbose_name='书籍类目')

	name = models.CharField(max_length=100, null=True, blank=True, verbose_name="书籍名称")
	press = models.CharField(max_length=100, null=True, blank=True, verbose_name="出版社")
	version = models.CharField(max_length=100, null=True, blank=True, verbose_name="书籍版本")

	price = models.FloatField(default=0, verbose_name="书籍价格")
	buyoutprice = models.FloatField(default=0, null=True, blank=True, verbose_name="一口价")

	ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
	photo = models.ImageField(upload_to="books/images/", null=True, blank=True, verbose_name="书籍图片")
	desc = UEditorField(imagePath="books/images/", width=1000, height=300,
						filePath="books/files/", default='', verbose_name=u"书籍描述信息", )
	nums = models.IntegerField(default=0, verbose_name="书籍数量")
	revoke = models.DateField(default=datetime.datetime.now() + datetime.timedelta(days=2), verbose_name="下架时间")
	status = models.IntegerField(default=1, choices=STATUS_CHOICES, verbose_name="书籍状态")
	add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = '书籍'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class BooksImage(models.Model):
	"""
	书籍轮播图
	"""
	books = models.ForeignKey(Books, verbose_name="书籍", related_name="images")
	image = models.ImageField(upload_to="books/images/", verbose_name="图片", null=True, blank=True)
	add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = '书籍图片'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.books.name

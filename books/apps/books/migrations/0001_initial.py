# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-02 21:50
from __future__ import unicode_literals

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='书籍名称')),
                ('press', models.CharField(blank=True, max_length=100, null=True, verbose_name='出版社')),
                ('version', models.CharField(blank=True, max_length=100, null=True, verbose_name='书籍版本')),
                ('price', models.FloatField(default=0, verbose_name='书籍价格')),
                ('buyoutprice', models.FloatField(blank=True, default=0, null=True, verbose_name='一口价')),
                ('ship_free', models.BooleanField(default=True, verbose_name='是否承担运费')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='books/images/', verbose_name='书籍图片')),
                ('desc', DjangoUeditor.models.UEditorField(default='', verbose_name='书籍描述信息')),
                ('nums', models.IntegerField(default=0, verbose_name='书籍数量')),
                ('revoke', models.DateField(default=datetime.datetime(2018, 4, 4, 21, 50, 9, 296638), verbose_name='下架时间')),
                ('status', models.IntegerField(choices=[(1, '书城'), (2, '征书墙'), (3, '竞拍'), (4, '下架')], default=1, verbose_name='书籍状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '书籍',
                'verbose_name_plural': '书籍',
            },
        ),
        migrations.CreateModel(
            name='BooksCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='类别名', max_length=30, verbose_name='类别名')),
                ('code', models.CharField(default='', help_text='类别code', max_length=30, verbose_name='类别code')),
                ('desc', models.TextField(default='', help_text='类别描述', verbose_name='类别描述')),
                ('category_type', models.IntegerField(choices=[(1, '一级类目'), (2, '二级类目'), (3, '三级类目')], help_text='类目级别', verbose_name='类目级别')),
                ('is_tab', models.BooleanField(default=False, help_text='是否导航', verbose_name='是否导航')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('parent_category', models.ForeignKey(blank=True, help_text='父目录', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_cat', to='books.BooksCategory', verbose_name='父类目级别')),
            ],
            options={
                'verbose_name': '书籍类别',
                'verbose_name_plural': '书籍类别',
            },
        ),
        migrations.CreateModel(
            name='BooksImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='books/images/', verbose_name='图片')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('books', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='books.Books', verbose_name='书籍')),
            ],
            options={
                'verbose_name': '书籍图片',
                'verbose_name_plural': '书籍图片',
            },
        ),
        migrations.AddField(
            model_name='books',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.BooksCategory', verbose_name='书籍类目'),
        ),
    ]

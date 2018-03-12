# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-01 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Terminology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, help_text='更新时间')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('classification', models.CharField(help_text='平台、模块、关键词', max_length=10, verbose_name='分类')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='软删除')),
            ],
            options={
                'verbose_name': '词库管理',
                'verbose_name_plural': '词库管理',
                'db_table': 'terminology',
            },
        ),
    ]

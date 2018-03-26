# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_role_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='has_backend',
        ),
        migrations.RemoveField(
            model_name='role',
            name='has_frontend',
        ),
        migrations.AddField(
            model_name='role',
            name='has_classification',
            field=models.BooleanField(default=False, verbose_name='类别管理'),
        ),
        migrations.AddField(
            model_name='role',
            name='has_data_display',
            field=models.BooleanField(default=True, verbose_name='数据展示'),
        ),
        migrations.AddField(
            model_name='role',
            name='has_problem',
            field=models.BooleanField(default=False, verbose_name='问题管理'),
        ),
        migrations.AddField(
            model_name='role',
            name='has_role',
            field=models.BooleanField(default=False, verbose_name='角色管理'),
        ),
        migrations.AddField(
            model_name='role',
            name='has_terminology',
            field=models.BooleanField(default=False, verbose_name='词库管理'),
        ),
        migrations.AddField(
            model_name='role',
            name='has_user',
            field=models.BooleanField(default=False, verbose_name='用户管理'),
        ),
    ]
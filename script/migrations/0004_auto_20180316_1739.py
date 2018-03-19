# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-16 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script', '0003_auto_20180315_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='script',
            name='path',
            field=models.CharField(default='', help_text='脚本存储路径', max_length=100, verbose_name='路径'),
        ),
    ]

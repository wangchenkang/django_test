# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-15 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='count',
            field=models.PositiveSmallIntegerField(default=0, help_text='执行脚本的个数', verbose_name='数量'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-23 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0007_auto_20180323_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='end_time',
            field=models.DateField(null=True, verbose_name='jira完成日期'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='start_time',
            field=models.DateField(verbose_name='jira创建日期'),
        ),
    ]

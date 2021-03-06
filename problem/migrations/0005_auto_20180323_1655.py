# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-23 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_auto_20180312_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='influenced_id',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='influenced_student',
        ),
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=models.CharField(max_length=400, null=True, verbose_name='问题描述'),
        ),
        migrations.RemoveField(
            model_name='problem',
            name='handler',
        ),
        migrations.AddField(
            model_name='problem',
            name='handler',
            field=models.CharField(max_length=150, null=True, verbose_name='处理人'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='reporter',
            field=models.CharField(max_length=10, verbose_name='jira报告人'),
        ),
    ]

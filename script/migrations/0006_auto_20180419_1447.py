# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-19 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script', '0005_auto_20180316_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='name',
            field=models.CharField(default='', max_length=2000, verbose_name='名称'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-03 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminology', '0005_auto_20180329_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='name',
            field=models.CharField(max_length=100, verbose_name='名称'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-08 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='软删除'),
        ),
    ]

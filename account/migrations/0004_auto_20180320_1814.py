# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-20 18:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20180319_1123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='group',
            new_name='groups',
        ),
    ]

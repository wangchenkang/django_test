# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-16 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem_classification', '0005_auto_20180315_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemcla',
            name='description',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='备注'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-08 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0003_auto_20180408_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontendlayout',
            name='page',
            field=models.PositiveSmallIntegerField(help_text='dashboard0, dashboard1, dashboard2', verbose_name='属于哪个页面'),
        ),
    ]
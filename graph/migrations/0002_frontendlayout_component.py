# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-04 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontendlayout',
            name='component',
            field=models.CharField(default='', max_length=50),
        ),
    ]
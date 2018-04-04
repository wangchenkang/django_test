# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-29 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terminology', '0003_module_platform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platform',
            name='module',
        ),
        migrations.AddField(
            model_name='module',
            name='platform',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='platforms', to='terminology.Platform', verbose_name='所属平台'),
            preserve_default=False,
        ),
    ]

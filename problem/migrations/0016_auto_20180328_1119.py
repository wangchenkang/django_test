# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-28 11:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem_classification', '0005_auto_20180315_1120'),
        ('problem', '0015_auto_20180328_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='classification',
        ),
        migrations.AddField(
            model_name='problem',
            name='classification',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='problem_classification.ProblemCla', verbose_name='对应问题分类'),
            preserve_default=False,
        ),
    ]

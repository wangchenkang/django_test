# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-28 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cycle_task', '0004_auto_20180328_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycletask',
            name='classification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='problem_classification.ProblemCla', verbose_name='对应问题分类'),
        ),
    ]

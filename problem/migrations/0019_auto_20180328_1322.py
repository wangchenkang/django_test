# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-28 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0018_auto_20180328_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='classification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem_classification.ProblemCla', verbose_name='对应问题分类'),
        ),
    ]
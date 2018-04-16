# coding=utf-8
from django.db import models
from common.modelbase import (MyModelBase, MyCUModelBase, MyCModelBase,
                              TinyIntegerField, PositiveTinyIntegerField,
                              PositiveBigIntegerField)
from script.models import Script


class ProblemCla(MyCUModelBase):
    """
    类别管理
    """
    name = models.CharField('名称', max_length=100, unique=True)
    is_deleted = models.BooleanField('软删除', default=False)
    is_active = models.BooleanField('可否使用', default=True)
    script = models.OneToOneField(Script, verbose_name='对应脚本', null=True)
    description = models.CharField('备注', max_length=200, default='', blank=True)

    class Meta:
        db_table = 'problem_cla'
        verbose_name = '类别管理'
        verbose_name_plural = '类别管理'

    def __str__(self):
        return "ProblemClassification of {}".format(self.name)

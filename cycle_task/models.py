# coding=utf-8
from django.db import models
from common.modelbase import (MyModelBase, MyCUModelBase, MyCModelBase,
                              TinyIntegerField, PositiveTinyIntegerField,
                              PositiveBigIntegerField)
from problem_classification.models import ProblemCla


class CycleTask(MyCUModelBase):
    """
    脚本管理
    """
    name = models.CharField('名称', max_length=100, unique=True)
    classification = models.OneToOneField(ProblemCla, verbose_name='对应问题分类')

    start_time = models.DateTimeField('启动时间', null=True)
    next_time = models.DateTimeField('下一次执行的时间', null=True,
                                     help_text='每次根据执行周期刷新，执行失败时设空')
    cycle = models.PositiveIntegerField('执行周期', default=0,
                                        help_text='单位是小时')

    count = models.PositiveIntegerField('执行次数', default=0,
                                        help_text='只是自己记下执行的次数')
    status = models.CharField('运行状态', max_length=10, default='停止',
                              help_text='停止、正常、失败')

    is_active = models.BooleanField('是否启用', default=True)
    is_deleted = models.BooleanField('软删除', default=False)

    description = models.CharField('备注信息', max_length=400, default='')

    class Meta:
        db_table = 'cycle_task'
        verbose_name = '脚本管理'
        verbose_name_plural = '脚本管理'

    def __str__(self):
        return "CycleTask of {}".format(self.name)

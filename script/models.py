# coding=utf-8
from django.db import models
from common.modelbase import (MyModelBase, MyCUModelBase, MyCModelBase,
                              TinyIntegerField, PositiveTinyIntegerField,
                              PositiveBigIntegerField)


class Script(MyCUModelBase):
    """
    脚本管理
    """
    name = models.CharField('名称', max_length=50, default='')
    path = models.CharField('路径', max_length=100, default='',
                            help_text='脚本存储路径')
    run_command = models.CharField('命令', max_length=100,
                                   help_text='脚本启动命令')
    is_deleted = models.BooleanField('软删除', default=False)
    count = models.PositiveSmallIntegerField('数量', default=0,
                                             help_text='执行脚本的个数')

    class Meta:
        db_table = 'script'
        verbose_name = '脚本管理'
        verbose_name_plural = '脚本管理'

    def __str__(self):
        return "Script of {}".format(self.id)

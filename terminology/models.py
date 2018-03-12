# coding=utf-8
from django.db import models
from common.modelbase import (MyModelBase, MyCUModelBase, MyCModelBase,)


class Terminology(MyCUModelBase):
    """
    词库管理
    """
    name = models.CharField('名称', max_length=100)
    classification = models.CharField('分类', max_length=10,
                                      help_text='平台、模块、关键词')
    is_deleted = models.BooleanField('软删除', default=False)

    class Meta:
        db_table = 'terminology'
        verbose_name = '词库管理'
        verbose_name_plural = '词库管理'
        unique_together = (('name', 'classification'),)

    def __str__(self):
        return "Terminology of {} - {}".format(self.name, self.classification)

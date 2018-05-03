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


class Platform(MyCUModelBase):
    """
    平台管理
    """
    name = models.CharField('名称', max_length=100)
    # module = models.ManyToManyField(Module, verbose_name='包含模块')
    is_deleted = models.BooleanField('软删除', default=False)

    class Meta:
        db_table = 'platform'
        verbose_name = '平台管理'
        verbose_name_plural = '平台管理'

    def __str__(self):
        return 'Platform of {}'.format(self.name)


class Module(MyCUModelBase):
    """
    模块管理
    """
    name = models.CharField('名称', max_length=100)
    is_deleted = models.BooleanField('软删除', default=False)
    platform = models.ForeignKey(Platform, related_name='platforms',
                                 verbose_name='所属平台',
                                 on_delete=models.CASCADE)

    class Meta:
        db_table = 'module'
        verbose_name = '模块管理'
        verbose_name_plural = '模块管理'
        unique_together = ('name', 'platform')

    def __str__(self):
        return 'Module of {}'.format(self.name)






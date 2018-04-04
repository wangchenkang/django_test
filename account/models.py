# coding=utf-8
from django.contrib.auth.models import Group
from django.db import models


class Role(models.Model):

    groups = models.OneToOneField(Group, verbose_name='分组',
                                  on_delete=models.CASCADE)
    has_data_display = models.BooleanField('数据展示', default=True)
    has_classification = models.BooleanField('类别管理', default=False)
    has_cycle_task = models.BooleanField('任务管理', default=False)
    has_problem = models.BooleanField('问题管理', default=False)
    has_terminology = models.BooleanField('词库管理', default=False)
    has_user = models.BooleanField('用户管理', default=False)
    has_role = models.BooleanField('角色管理', default=False)
    is_deleted = models.BooleanField('软删除', default=False)

    class Meta:
        db_table = 'role'
        verbose_name = '角色管理'
        verbose_name_plural = '角色管理'

    def __str__(self):
        return "Role of {}".format(self.groups.name)


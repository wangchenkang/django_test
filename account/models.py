# coding=utf-8
from django.contrib.auth.models import Group
from django.db import models


class Role(models.Model):

    group = models.OneToOneField(Group, verbose_name='分组')
    has_frontend = models.BooleanField('前台权限', default=True)
    has_backend = models.BooleanField('后台权限', default=False)
    is_deleted = models.BooleanField('软删除', default=False)

    class Meta:
        db_table = 'role'
        verbose_name = '角色管理'
        verbose_name_plural = '角色管理'

    def __str__(self):
        return "Role of {}".format(self.group.name)


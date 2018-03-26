# coding=utf-8
from django.db import models
from common.modelbase import (MyModelBase, MyCUModelBase, MyCModelBase,
                              TinyIntegerField, PositiveTinyIntegerField,
                              PositiveBigIntegerField)
from problem_classification.models import ProblemCla
from terminology.models import Terminology, Platform, Module


class UserInJira(models.Model):
    """
    记录 问题管理中的'处理人'、'报告人'
    """
    username = models.CharField('用户姓名', max_length=10, unique=True)
    # is_inner = models.BooleanField('是否是内部员工', default=True)
    # stu_num = PositiveBigIntegerField('jira中的问题学生的学号', null=True)

    class Meta:
        db_table = 'user_in_jira'
        verbose_name = '姓名管理'
        verbose_name_plural = '姓名管理'

    def __str__(self):
        return "UserInJira of {}".format(self.username)


class UniversityInJira(models.Model):
    """
    记录 问题管理中的'影响学校'
    """
    name = models.CharField('学校名称', max_length=30, unique=True)

    class Meta:
        db_table = 'university'
        verbose_name = '校名管理'
        verbose_name_plural = '校名管理'

    def __str__(self):
        return 'UniversityInJira of {}'.format(self.name)


class Problem(MyCUModelBase):
    """
    问题管理
    """
    jira_code = models.CharField('jira键值', max_length=100, unique=True)

    classification = models.ManyToManyField(ProblemCla, verbose_name='对应问题分类')
    platforms = models.ManyToManyField(Platform, verbose_name='所属平台',
                                       related_name='platform')
    modules = models.ManyToManyField(Module, verbose_name='所属模块',
                                     related_name='modules')
    # keywords = models.ManyToManyField(Terminology, verbose_name='所属关键词',
    #                                   related_name='keywords')

    tackle_status = models.BooleanField('处理状态', default=False,
                                        help_text='0未修复 1已修复，应根据end自动变')
    level = models.PositiveSmallIntegerField('问题评级')
    description = models.CharField('问题描述', max_length=400, null=True)

    start_time = models.DateField('jira创建日期')
    end_time = models.DateField('jira完成日期', null=True)
    process_time = models.PositiveIntegerField('处理时长', default=0, null=True,
                                               help_text='单位是分钟，应在有end时计算')

    reporter = models.OneToOneField(UserInJira, verbose_name='jira报告人',
                                    related_name='reporter')
    handler = models.ManyToManyField(UserInJira, verbose_name='处理人',
                                     related_name='handler',
                                     help_text='可能有多个人')
    # reporter = models.CharField('jira报告人', max_length=10)
    # handler = models.CharField('处理人', max_length=150, null=True)

    influenced_university = models.ManyToManyField(
        UniversityInJira, verbose_name='影响学校', null=True,
        related_name='influenced_university')
    # influenced_id = models.ManyToManyField(UserInJira, verbose_name='影响用户id',
    #                                        related_name='influenced_id')
    # influenced_student = models.ManyToManyField(UserInJira,
    #                                             related_name='influenced_student',
    #                                             verbose_name='影响学生姓名')

    is_deleted = models.BooleanField('软删除', default=False)

    rdm = models.OneToOneField(UserInJira, verbose_name='研发负责人',
                               related_name='rdm', null=True)
    pm = models.OneToOneField(UserInJira, verbose_name='产品负责人',
                              related_name='pm', null=True)

    class Meta:
        db_table = 'problem'
        verbose_name = '问题管理'
        verbose_name_plural = '问题管理'

    def __str__(self):
        return "Problem of {}".format(self.jira_code)

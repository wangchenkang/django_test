from django.db import models

from common.modelbase import MyCUModelBase


class FrontendLayout(MyCUModelBase):
    """
    主要为了存前端图表的布局格式配置信息
    """

    page = models.PositiveSmallIntegerField(
        '属于哪个页面', help_text='dashboard0, dashboard1, dashboard2')
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    i = models.CharField(max_length=50)
    chart_type = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    component = models.CharField(max_length=50, default='')
    y_field = models.CharField(max_length=50, default='')
    x_field = models.CharField(max_length=50, default='')
    y_name = models.CharField(max_length=50, default='')
    x_name = models.CharField(max_length=50, default='')
    y_unit = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'frontend_layout'
        verbose_name = '前端展示用图表位置'
        verbose_name_plural = '前端展示用图表位置'

    def __str__(self):
        return "FrontendLayout of {}".format(self.title)

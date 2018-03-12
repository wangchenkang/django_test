# coding=utf-8
from django.db import models


class MyModelBase(models.Model):
    """
    extend the length of id
    """
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID')

    class Meta:
        abstract = True


class MyCUModelBase(models.Model):
    """
    db model base class contains two default fields
    create_time and update_time
    """
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID')
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    updated = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        abstract = True


class MyCModelBase(models.Model):
    """
    db model base class contains two default fields create_time
    """
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID')
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    class Meta:
        abstract = True


class TinyIntegerField(models.SmallIntegerField):
    """
    -128~127
    """
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    """
    0~255
    """
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint UNSIGNED"
        else:
            return super(PositiveTinyIntegerField, self).db_type(connection)


class PositiveBigIntegerField(models.BigIntegerField):
    """
    bigint(20)
    0~18446744073709551615
    """
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'bigint UNSIGNED'
        else:
            return super(PositiveBigIntegerField, self).db_type(connection)

    def formfield(self, **kwargs):
        defaults = {'min_value': 0,
                    'max_value': models.BigIntegerField.MAX_BIGINT * 2 - 1}
        defaults.update(kwargs)
        return super(PositiveBigIntegerField, self).formfield(**defaults)

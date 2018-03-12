from __future__ import unicode_literals

from django.db import models


class PermissionsUser(models.Model):
    name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=100)
    email = models.CharField(max_length=75)
    phone = models.CharField(max_length=20)
    is_active = models.CharField(max_length=1)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    real_name = models.CharField(max_length=50, blank=True, null=True)
    is_super = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'permissions_user'

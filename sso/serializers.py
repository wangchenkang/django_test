# coding=utf-8
from rest_framework import serializers
from sso.models import PermissionsUser


class SsoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True)

    class Meta:
        model = PermissionsUser
        fields = ('name',)


class SsoRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionsUser
        fields = ('id', 'name',)

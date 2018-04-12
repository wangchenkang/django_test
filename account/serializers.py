# coding=utf-8
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import Role
from terminology.models import Terminology


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class AccountSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'groups')


class AccountCreateSerializer(serializers.ModelSerializer):
    groups = serializers.ListField(
        child=serializers.IntegerField())

    def validate_groups(self, value):
        g = Group.objects.filter(id__in=value).count()
        if len(value) != g:
            raise ValidationError('传入的group_id有问题')
        else:
            return value

    class Meta:
        model = User
        fields = ('username', 'groups')


class AccountUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.ListField(
        child=serializers.IntegerField())

    def validate_groups(self, value):
        g = Group.objects.filter(id__in=value).count()
        if len(value) != g:
            raise ValidationError('传入的group_id有问题')
        else:
            return value

    class Meta:
        model = User
        fields = ('groups',)


class RoleSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(read_only=True,
                                          slug_field='name')

    class Meta:
        model = Role
        fields = ('id', 'groups')


class RoleCreateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=80)

    class Meta:
        model = Role
        fields = ('name', 'has_data_display', 'has_classification',
                  'has_cycle_task', 'has_problem', 'has_terminology',
                  'has_user', 'has_role')


class RoleRetrieveSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=False, read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'groups', 'has_data_display', 'has_classification',
                  'has_cycle_task', 'has_problem', 'has_terminology',
                  'has_user', 'has_role')


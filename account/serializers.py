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

    # groups = serializers.SlugRelatedField(slug_field='name',
    #                                       many=True,
    #                                       read_only=True)

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
    group = serializers.SlugRelatedField(read_only=True,
                                         slug_field='name')

    class Meta:
        model = Role
        fields = ('id', 'group', 'has_frontend', 'has_backend')


class RoleCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=80)
    has_frontend = serializers.BooleanField(default=True)
    has_backend = serializers.BooleanField(default=False)

    def create(self, validated_data):
        super(RoleCreateSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(RoleCreateSerializer, self).update(instance, validated_data)

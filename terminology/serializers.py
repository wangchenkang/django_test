# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from terminology.models import Terminology


class TerminologyListSerializer(serializers.Serializer):

    cla = serializers.CharField(max_length=10)

    def validate_cla(self, value):
        if value not in ('平台', '模块', '关键词'):
            raise ValidationError('This value is not acceptable.')
        return value

    def create(self, validated_data):
        super(TerminologyListSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(TerminologyListSerializer, self).update(instance, validated_data)


class TerminologyCreateSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    classification = serializers.CharField(max_length=10)

    def validate_classification(self, value):
        if value not in ('平台', '模块', '关键词'):
            raise ValidationError('This value is not acceptable.')
        return value

    def create(self, validated_data):
        super(TerminologyCreateSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(TerminologyCreateSerializer, self).update(instance, validated_data)


# class TerminologyCreateSerializer(serializers.ModelSerializer):
#
#     # name = serializers.CharField(max_length=100)
#     # classification = serializers.CharField(max_length=10)
#
#     def validate_classification(self, value):
#         if value not in ('平台', '模块', '关键词'):
#             raise ValidationError('This value is not acceptable.')
#         return value
#
#     class Meta:
#         model = Terminology
#         fields = ('name', 'classification')


class TerminologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Terminology
        fields = ('id', 'name', 'created', 'updated')


class TerminologyRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Terminology
        fields = ('id', 'name')


class TerminologyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Terminology
        fields = ('name',)



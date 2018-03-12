# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from problem_classification.models import ProblemCla


class ProblemClaCreateSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        super(ProblemClaCreateSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(ProblemClaCreateSerializer, self).update(instance, validated_data)


class ProblemClaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemCla
        fields = ('id', 'name', 'is_active', 'script_id')


class ProblemClaRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemCla
        fields = ('id', 'name')


class ProblemClaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemCla
        fields = ('name',)



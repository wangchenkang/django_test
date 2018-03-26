# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from problem_classification.models import ProblemCla
from script.models import Script


# class ScriptCreateSer(serializers.ModelSerializer):
#     class Meta:
#         model = Script
#         fields = ('count',)
from terminology.models import Module


class ProblemClaCreateSerializer(serializers.ModelSerializer):

    run_command = serializers.CharField(max_length=100)

    class Meta:
        model = ProblemCla
        fields = ('name', 'is_active', 'description', 'script', 'run_command')


class ScriptListSer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('id', 'count')


class ProblemClaSerializer(serializers.ModelSerializer):
    script = ScriptListSer()

    class Meta:
        model = ProblemCla
        fields = ('id', 'name', 'is_active', 'script',)


class ScriptRetriveSer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('id', 'run_command', 'name')


class ProblemClaRetrieveSerializer(serializers.ModelSerializer):
    script = ScriptRetriveSer()

    class Meta:
        model = ProblemCla
        fields = ('id', 'name', 'is_active', 'description', 'script')


class ProblemClaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemCla
        fields = ('name',)


class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ('id', 'name')

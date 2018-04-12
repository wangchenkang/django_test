# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cycle_task.models import CycleTask
from problem_classification.models import ProblemCla
from terminology.models import Terminology, Platform, Module


class ProblemClaSer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCla
        fields = ('id', 'name')


class CycleTaskListSerializer(serializers.ModelSerializer):
    classification = ProblemClaSer()

    class Meta:
        model = CycleTask
        fields = ('id', 'name', 'classification', 'start_time',
                  'status', 'is_active')


class CycleTaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CycleTask
        fields = ('name', 'classification', 'start_time', 'cycle',
                  'is_active', 'description')


class CycleTaskRetrieveSerializer(serializers.ModelSerializer):
    # classification = ProblemClaSer()

    class Meta:
        model = CycleTask
        fields = ('id', 'name', 'classification', 'start_time', 'cycle',
                  'is_active', 'description')


class CycleTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = CycleTask
        fields = ('id', 'name', 'created', 'updated')




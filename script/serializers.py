# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from problem_classification.models import ProblemCla
from script.models import Script


# class ProblemClaCreateSerializer(serializers.Serializer):
#
#     name = serializers.CharField(max_length=100)
#     is_active = serializers.BooleanField()
#     description = serializers.CharField(max_length=200)
#     run_command = serializers.CharField(max_length=100)
#
#     def create(self, validated_data):
#         super(ProblemClaCreateSerializer, self).create(validated_data)
#
#     def update(self, instance, validated_data):
#         super(ProblemClaCreateSerializer, self).update(instance, validated_data)


class ScriptCreateSer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('count',)


class ProblemClaCreateSerializer(serializers.ModelSerializer):

    run_command = serializers.CharField(max_length=100)

    class Meta:
        model = ProblemCla
        fields = ('name', 'is_active', 'description', 'script', 'run_command')

    def create(self, validated_data):
        script_id = validated_data.pop('script')
        run_command = validated_data.pop('run_command')
        problem_cla = ProblemCla.objects.create(**validated_data)
        if script_id:
            problem_cla.script = Script.objects.get(pk=script_id)
        else:
            script = Script.objects.create(run_command=run_command)
            problem_cla.script = script
        problem_cla.save()


class ScriptListSer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('id', 'count')


class ProblemClaSerializer(serializers.ModelSerializer):
    script = ScriptListSer()

    class Meta:
        model = ProblemCla
        fields = ('id', 'name', 'is_active', 'script',)


class ProblemClaRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemCla
        fields = ('id', 'name')


class ProblemClaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemCla
        fields = ('name',)



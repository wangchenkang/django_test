# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from problem.models import Problem, UserInJira, UniversityInJira
from problem_classification.models import ProblemCla
from terminology.models import Platform, Module


class ProblemCreateSerializer(serializers.ModelSerializer):

    description = serializers.CharField(allow_blank=True)
    platforms = serializers.ListField(allow_empty=True)
    reporter = serializers.CharField(max_length=10)
    handler = serializers.CharField(allow_blank=True)
    influenced_university = serializers.CharField(allow_blank=True)
    rdm = serializers.CharField(allow_blank=True)
    pm = serializers.CharField(allow_blank=True)

    class Meta:
        model = Problem
        fields = ('jira_code', 'classification', 'platforms', 'modules',
                  'tackle_status', 'level', 'description',
                  'start_time', 'end_time', 'reporter', 'handler',
                  'influenced_university', 'rdm', 'pm')


class ProblemQuerySerializer(serializers.Serializer):

    jira_code = serializers.ListField(required=False)
    start_time = serializers.DateField(required=False)
    end_time = serializers.DateField(required=False)
    reporter = serializers.ListField(child=serializers.IntegerField(),
                                     required=False)
    handler = serializers.ListField(child=serializers.IntegerField(),
                                    required=False)
    rdm = serializers.ListField(child=serializers.IntegerField(),
                                required=False)
    pm = serializers.ListField(child=serializers.IntegerField(),
                               required=False)

    def get_data(self):
        return self._validated_data

    def validate_jira_code(self, value):
        return {'jira_code__icontains': value}

    def validate_start_time(self, value):
        return {'start_time__gte': value}

    def validate_end_time(self, value):
        return {'end_time__lte': value}

    def validate_reporter(self, value):
        return {'reporter__in': value}

    def validate_handler(self, value):
        return {'handler__id__in': value}

    def validate_rdm(self, value):
        return {'rdm__in': value}

    def validate_pm(self, value):
        return {'pm__in': value}

    def create(self, validated_data):
        super(ProblemQuerySerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(ProblemQuerySerializer, self).update(instance, validated_data)


class ProblemClaSer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCla
        fields = ('id', 'name')


class PlatformSer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name')


class ModuleSer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name')


class UserInJiraSer(serializers.ModelSerializer):
    class Meta:
        model = UserInJira
        fields = ('id', 'username')


class UniversityInJiraSer(serializers.ModelSerializer):
    class Meta:
        model = UniversityInJira
        fields = ('id', 'name')


class ProblemSerializer(serializers.ModelSerializer):
    platforms = PlatformSer(many=True, read_only=True)
    modules = ModuleSer(many=True, read_only=True)
    rdm = UserInJiraSer()
    pm = UserInJiraSer()

    class Meta:
        model = Problem
        fields = ('id', 'jira_code', 'platforms', 'modules', 'process_time',
                  'rdm', 'pm', 'start_time', 'end_time')


class ProblemRetrieveSerializer(serializers.ModelSerializer):
    classification = ProblemClaSer(many=True, read_only=True)
    platforms = PlatformSer(many=True, read_only=True)
    modules = ModuleSer(many=True, read_only=True)
    reporter = UserInJiraSer()
    handler = UserInJiraSer(many=True, read_only=True)
    influenced_university = UniversityInJiraSer(many=True, read_only=True)
    rdm = UserInJiraSer()
    pm = UserInJiraSer()

    class Meta:
        model = Problem
        fields = ('id', 'jira_code', 'classification', 'platforms', 'modules',
                  'tackle_status', 'level', 'description',
                  'start_time', 'end_time', 'reporter', 'handler',
                  'influenced_university', 'rdm', 'pm')


class ProblemClaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('name',)



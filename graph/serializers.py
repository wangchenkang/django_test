import json
import re
from rest_framework import serializers


class GraphQuerySerializer(serializers.Serializer):

    jira_code = serializers.ListField(required=False)
    classification = serializers.ListField(required=False)

    start_time_1 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    start_time_2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    end_time_1 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    end_time_2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    module_platform = serializers.ListField(required=False)
    platform = serializers.ListField(required=False)
    level = serializers.ListField(required=False)
    tackle_status = serializers.ListField(required=False)

    reporter = serializers.ListField(required=False)
    handler = serializers.ListField(required=False)
    influenced_university = serializers.ListField(required=False)

    def get_data(self):
        return self._validated_data

    def validate_jira_code(self, value):
        return [{'id__in': value}]

    def validate_classification(self, value):
        return [{'classification_id__in': value}]

    def validate_start_time_1(self, value):
        return json.dumps([{'start_time__gte': value}])

    def validate_start_time_2(self, value):
        return json.dumps([{'start_time__lte': value}])

    def validate_end_time_1(self, value):
        return json.dumps([{'end_time__gte': value}])

    def validate_end_time_2(self, value):
        return json.dumps([{'end_time__lte': value}])

    def validate_module_platform(self, value):
        res_list = []
        for i in value:
            m, p = i.split('/')
            res_list.append(m)
        return [{'modules__id__in': res_list}]

    def validate_platform(self, value):
        return [{'platforms__id__in': value}]

    def validate_level(self, value):
        return [{'level__in': value}]

    def validate_tackle_status(self, value):
        return [{'tackle_status__in': value}]

    def validate_reporter(self, value):
        return [{'reporter_id__in': value}]

    def validate_handler(self, value):
        return [{'handler__id__in': value}]

    def validate_influenced_university(self, value):
        return [{'influenced_university__id__in': value}]

    def create(self, validated_data):
        super(GraphQuerySerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(GraphQuerySerializer, self).update(instance, validated_data)

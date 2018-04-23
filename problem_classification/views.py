# coding=utf-8
import copy

from django.db import transaction
from rest_framework import mixins, viewsets, status, filters
from rest_framework.response import Response

from common.paginations import Pagination20
from problem_classification.models import ProblemCla
from problem_classification.serializers import ProblemClaSerializer, \
    ProblemClaCreateSerializer, ProblemClaRetrieveSerializer
from script.models import Script


class ProblemClaView(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    问题分类管理CRUD
    """
    queryset = ProblemCla.objects.filter(is_deleted=False)
    serializer_class = ProblemClaSerializer
    pagination_class = Pagination20
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ser = ProblemClaCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        if not request.data['script']:
            script_id = Script.objects.create(
                run_command=ser.data['run_command']).id
        else:
            script_id = request.data['script']
            s = Script.objects.get(pk=script_id)
            s.run_command = ser.data['run_command']
            s.save()

        ProblemCla.objects.create(
            name=ser.data['name'],
            is_active=ser.data['is_active'],
            description=ser.data['description'],
            script_id=script_id,
        )

        return Response(data={'error_code': 0,
                              'data': {
                                  'script': script_id
                              }},
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            p = self.get_paginated_response(ser.data)
            p.update({'error_code': 0})
            return Response(data=p,
                            status=status.HTTP_200_OK)

        ser = ProblemClaSerializer(queryset, many=True)

        return Response(data={'error_code': 0,
                              'data': ser.data},
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ProblemClaRetrieveSerializer
        instance = self.get_object()

        ser = self.get_serializer(instance)
        # ser.data['script']['name'] = ser.data['script']['name'].split(',')
        data = copy.deepcopy(ser.data)
        if instance.script:
            data['run_command'] = instance.script.run_command
        else:
            data['run_command'] = ''

        return Response(data={'error_code': 0,
                              'data': data},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ProblemClaCreateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 为了处理只更新is_active字段
        if request.query_params.get('m', '') != 'patch':
            ser = self.get_serializer(instance, data=request.data, partial=partial)
            ser.is_valid(raise_exception=True)

            if ser.initial_data.get('script', ''):
                s = Script.objects.get(pk=ser.initial_data['script'])
                s.run_command = ser.initial_data.get('run_command', '')
                instance.script = s
                instance.script.save()
            else:
                instance.script = None

            self.perform_update(ser)
        else:
            instance.is_active = request.data.get('is_active', False)
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return Response(data={'error_code': 0,
                                  'data': {}},
                            status=status.HTTP_200_OK)

        instance.is_deleted = True
        instance.save()
        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)

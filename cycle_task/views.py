# coding=utf-8
import os
from django.db import IntegrityError, transaction
from rest_framework import mixins, viewsets, status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from common.paginations import Pagination20
from cycle_task.models import CycleTask
from cycle_task.serializers import \
    CycleTaskCreateSerializer, CycleTaskSerializer, CycleTaskListSerializer, \
    ProblemClaSer, CycleTaskRetrieveSerializer
from problem_classification.models import ProblemCla


class TestView(APIView):
    http_method_names = ('get',)

    def get(self, request):
        # :todo 要做实验 创建目录、删除、下文件
        import errno, shutil
        db_path = '{}/new/hunting_tracker/cycle_task/'.format('/tmp')
        try:
            os.makedirs(db_path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                shutil.rmtree(db_path)
                os.makedirs(db_path)

        return Response(data={}, status=status.HTTP_200_OK)


class CycleTaskView(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    任务管理CRUD
    """
    queryset = CycleTask.objects.filter(is_deleted=False).order_by('id')
    serializer_class = CycleTaskSerializer
    pagination_class = Pagination20
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def create(self, request, *args, **kwargs):
        ser = CycleTaskCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        CycleTask.objects.create(
            name=ser.data['name'],
            classification_id=ser.data['classification'],
            start_time=ser.data['start_time'],
            next_time=ser.data['start_time'],
            cycle=ser.data['cycle'],
            is_active=ser.data['is_active'],
            description=ser.data['description'],
        )

        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        self.serializer_class = CycleTaskListSerializer
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            p = self.get_paginated_response(ser.data)
            p.update({'error_code': 0})
            return Response(data=p,
                            status=status.HTTP_200_OK)

        ser = self.get_serializer(queryset, many=True)

        return Response(data={'error_code': 0,
                              'data': ser.data},
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CycleTaskRetrieveSerializer
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(data={'error_code': 0,
                              'data': serializer.data},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.serializer_class = CycleTaskCreateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 为了处理只更新is_active字段
        if request.query_params.get('m', '') != 'patch':
            ser = self.get_serializer(instance, data=request.data, partial=partial)
            ser.is_valid(raise_exception=True)

            self.perform_update(ser)

            instance.next_time = ser.data['start_time']
            instance.status = '停止'
            instance.count = 0
        else:
            instance.is_active = request.data.get('is_active')
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


class AvailableProblemClaView(GenericAPIView):
    http_method_names = ('get',)
    queryset = ProblemCla.objects.filter(
        is_active=True, is_deleted=False).order_by('id')
    serializer_class = ProblemClaSer
    pagination_class = Pagination20
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get(self, request):
        # 任务管理模块中，在create、update操作时，选'执行类别'时，
        # 由于是OneToOneField，所以在此过滤掉不可选的
        cycle_task = CycleTask.objects.filter(
            is_deleted=False).values_list('classification')

        cycle_task_set = set(ct[0] for ct in cycle_task)

        problem_cla = ProblemCla.objects.filter(
            is_active=True, is_deleted=False)

        queryset = self.filter_queryset(problem_cla)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        res_list = []
        for pc in queryset:
            if pc.id in cycle_task_set:
                res_list.append({
                    'id': pc.id,
                    'name': pc.name,
                    'is_used': True,
                })
            else:
                res_list.append({
                    'id': pc.id,
                    'name': pc.name,
                    'is_used': False,
                })

        # p = self.get_paginated_response(res_list)
        # p.update({'error_code': 0})
        return Response(data={'error_code': 0, 'data': res_list},
                        status=status.HTTP_200_OK)

        # ser = self.get_serializer(queryset, many=True)
        #
        # return Response(data={'error_code': 0,
        #                       'data': ser.data},
        #                 status=status.HTTP_200_OK)


class CycleTaskResultView(APIView):
    http_method_names = ('post',)

    def post(self, request):
        CycleTask.objects.filter(pk=request.data.get('id')).update(
            result=request.data.get('data')
        )

        return Response(data={}, status=status.HTTP_200_OK)

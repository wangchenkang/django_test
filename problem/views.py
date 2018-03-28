# coding=utf-8
import operator
from functools import reduce
from datetime import datetime
import django_filters
import re
from django.db import IntegrityError, transaction
from django.db import models
from rest_framework import mixins, viewsets, status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from common.paginations import Pagination20
from problem.models import Problem, UserInJira, UniversityInJira
from problem.serializers import ProblemSerializer, ProblemQuerySerializer, \
    ProblemCreateSerializer, ProblemRetrieveSerializer
from problem_classification.serializers import ProblemClaSerializer, \
    ProblemClaCreateSerializer, ProblemClaUpdateSerializer, \
    ProblemClaRetrieveSerializer, ModuleSerializer
from terminology.models import Module


class ProblemView(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    问题管理CRUD
    """
    queryset = Problem.objects.filter(is_deleted=False).order_by('id')
    serializer_class = ProblemSerializer
    pagination_class = Pagination20
    # filter_backends = (filters.SearchFilter,
    #                    django_filters.rest_framework.DjangoFilterBackend)
    # search_fields = ('jira_code',)

    def create(self, request, *args, **kwargs):
        ser = ProblemCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        regex = re.compile(r'(，|,|\.|。|;|、|；)')
        clean_sep = re.sub(regex, ',', ser.data['handler']).split(',')
        username_set = set(clean_sep)

        clean_sep = re.sub(regex, ',', ser.data['influenced_university']).split(',')
        univeristy_set = set(clean_sep)

        reporter, _ = UserInJira.objects.get_or_create(
            username=ser.data['reporter'])

        rdm, _ = UserInJira.objects.get_or_create(
            username=ser.data['rdm'])

        pm, _ = UserInJira.objects.get_or_create(
            username=ser.data['pm'])

        uij_id_list = []
        for u in username_set:
            uij, _ = UserInJira.objects.get_or_create(username=u)
            uij_id_list.append(uij.id)

        unij_id_list = []
        for u in univeristy_set:
            unij, _ = UniversityInJira.objects.get_or_create(name=u)
            unij_id_list.append(unij.id)

        with transaction.atomic():
            problem = Problem.objects.create(
                jira_code=ser.data['jira_code'],
                tackle_status=ser.data['tackle_status'],
                level=ser.data['level'],
                description=ser.data['description'],
                start_time=ser.data['start_time'],
                end_time=ser.data['end_time'],
                reporter=reporter,
                rdm=rdm,
                pm=pm,
            )

            problem.classification.add(*ser.data['classification'])
            problem.platforms.add(*ser.data['platforms'])
            problem.modules.add(*ser.data['modules'])
            problem.handler.add(*uij_id_list)
            problem.influenced_university.add(*unij_id_list)

            if ser.data['end_time']:
                start_time = datetime.strptime(ser.data['start_time'], '%Y-%m-%d')
                end_time = datetime.strptime(ser.data['end_time'], '%Y-%m-%d')
                if (end_time - start_time).days > 0:
                    problem.process_time = (end_time - start_time).days * 24
                    problem.save()

        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        ser = ProblemQuerySerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)

        queries = models.Q()
        for k, v in ser.get_data().items():
            [(k2, v2)] = v.items()
            if isinstance(v2, list):
                if len(v2) == 0:
                    continue
                elif len(v2) == 1:
                    if '__in' in k2:
                        queries &= models.Q(**{k2: v2})
                    else:
                        queries &= models.Q(**{k2: v2[0]})
                elif len(v2) > 1:
                    # 同一个搜索条件内的用或
                    tmp_q = 0
                    for q in [models.Q(**{k2: i}) for i in v2]:
                        if tmp_q == 0:
                            tmp_q = q
                        else:
                            tmp_q |= q
                    queries &= tmp_q
            else:
                queries &= models.Q(**v)

        if len(queries.children):
            queryset = self.queryset.filter(queries)
        else:
            queryset = self.queryset

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
        self.serializer_class = ProblemRetrieveSerializer
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(data={'error_code': 0,
                              'data': serializer.data},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ProblemCreateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        ser = self.get_serializer(instance, data=request.data, partial=partial)
        ser.is_valid(raise_exception=True)

        regex = re.compile(r'(，|,|\.|。|;|、|；)')
        clean_sep = re.sub(regex, ',', ser.initial_data['handler']).split(',')
        username_set = set(clean_sep)

        clean_sep = re.sub(regex, ',',
                           ser.initial_data['influenced_university']).split(',')
        univeristy_set = set(clean_sep)

        reporter, _ = UserInJira.objects.get_or_create(
            username=ser.initial_data['reporter'])

        rdm, _ = UserInJira.objects.get_or_create(
            username=ser.initial_data['rdm'])

        pm, _ = UserInJira.objects.get_or_create(
            username=ser.initial_data['pm'])

        uij_id_list = []
        for u in username_set:
            uij, _ = UserInJira.objects.get_or_create(username=u)
            uij_id_list.append(uij.id)

        unij_id_list = []
        for u in univeristy_set:
            unij, _ = UniversityInJira.objects.get_or_create(name=u)
            unij_id_list.append(unij.id)

        with transaction.atomic():
            instance.jira_code = ser.initial_data['jira_code']
            instance.tackle_status = ser.initial_data['tackle_status']
            instance.level = ser.initial_data['level']
            instance.description = ser.initial_data['description']
            instance.start_time = ser.initial_data['start_time']
            instance.end_time = ser.initial_data['end_time']
            instance.reporter = reporter
            instance.rdm = rdm
            instance.pm = pm

            instance.classification.clear()
            instance.platforms.clear()
            instance.modules.clear()
            instance.handler.clear()
            instance.influenced_university.clear()

            instance.classification.add(*ser.initial_data['classification'])
            instance.platforms.add(*ser.initial_data['platforms'])
            instance.modules.add(*ser.initial_data['modules'])
            instance.handler.add(*uij_id_list)
            instance.influenced_university.add(*unij_id_list)

            if ser.initial_data['end_time']:
                instance.process_time = (instance.updated - instance.created
                                         ).seconds / 3600

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


class Platform2Module(APIView):
    http_method_names = ('get',)

    def get(self, request):
        """
        根据platform_id(平台)筛选出可以选择的module(模块)
        :param request:
        :return:
        """
        try:
            platform_ids = list(
                map(int, request.query_params.get('q', '').split(',')))
        except:
            return Response(data={'error_code': 0,
                                  'data': []},
                            status=status.HTTP_200_OK)

        modules = Module.objects.filter(platform__in=platform_ids)

        data = []
        for m in modules:
            data.append({
                'id': m.id,
                'name': m.name,
            })

        return Response(data={'error_code': 0,
                              'data': data},
                        status=status.HTTP_200_OK)

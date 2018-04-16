# coding=utf-8
from django.db import IntegrityError, transaction
from rest_framework import mixins, viewsets, status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from common.paginations import Pagination20
from terminology.models import Terminology, Platform, Module
from terminology.serializers import TerminologySerializer, \
    TerminologyListSerializer, TerminologyCreateSerializer, \
    TerminologyRetrieveSerializer, TerminologyUpdateSerializer, \
    PlatformSerializer, PlatformCreateUpdateSerializer, ModuleSerializer, \
    ModuleCreateUpdateSerializer, PlatformRetrieveSerializer


class TerminologyView(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    词库管理CRUD
    """
    queryset = Terminology.objects.filter(is_deleted=False).order_by('id')
    serializer_class = TerminologySerializer
    pagination_class = Pagination20

    def create(self, request, *args, **kwargs):
        ser = TerminologyCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        Terminology.objects.create(name=ser.data['name'],
                                   classification=ser.data['classification'])

        return Response(data={'error_code': 0,
                              'data': ser.data},
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        ser = TerminologyListSerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)

        cla = ser.data['cla']
        q = ser.data.get('q', None)

        if q:
            queryset = self.queryset.filter(classification=cla,
                                            name__icontains=q)
        else:
            queryset = self.queryset.filter(classification=cla)

        page = self.paginate_queryset(queryset)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            p = self.get_paginated_response(ser.data)
            p.update({'error_code': 0})
            return Response(data=p,
                            status=status.HTTP_200_OK)

        ser = TerminologySerializer(queryset, many=True)

        return Response(data={'error_code': 0,
                              'data': ser.data},
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TerminologyRetrieveSerializer
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(data={'error_code': 0,
                              'data': serializer.data},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.serializer_class = TerminologyUpdateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data={'error_code': 0,
                              'data': serializer.data},
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


class PlatformView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    平台管理CRUD
    """
    queryset = Platform.objects.filter(is_deleted=False).order_by('id')
    serializer_class = PlatformSerializer
    pagination_class = Pagination20
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def create(self, request, *args, **kwargs):
        ser = PlatformCreateUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        with transaction.atomic():
            pf = Platform.objects.create(name=ser.data['name'])
            created_list = []
            for i in ser.data['module']:
                created_list.append(Module(name=i['name'], platform=pf))
            if created_list:
                Module.objects.bulk_create(created_list)

        return Response(data={'error_code': 0,
                              'data': {}},
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

        ser = self.get_serializer(queryset, many=True)
        return Response(data={'error_code': 0,
                              'data': ser.data},
                        status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        pf = self.get_object()
        modules = Module.objects.filter(
            platform=pf).values('id', 'name', 'is_deleted')

        return Response(data={'error_code': 0,
                              'data': {
                                  'id': pf.id,
                                  'name': pf.name,
                                  'module': modules
                              }},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.serializer_class = PlatformCreateUpdateSerializer
        partial = kwargs.pop('partial', False)
        pf = self.get_object()

        ser = self.get_serializer(pf, data=request.data,
                                  partial=partial)
        ser.is_valid(raise_exception=True)

        pf.name = ser.data['name']
        pf.save()

        for i in request.data['module']:
            Module.objects.filter(pk=i['id']).update(is_deleted=i['is_deleted'])

        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            pf = self.get_object()
        except Exception:
            return Response(data={'error_code': 0,
                                  'data': {}},
                            status=status.HTTP_200_OK)

        pf.is_deleted = True
        pf.save()
        Module.objects.filter(platform=pf).update(is_deleted=True)

        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)


class ModuleView(mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    模块管理
    """
    queryset = Module.objects.filter(is_deleted=False).order_by('id')
    serializer_class = ModuleSerializer
    pagination_class = Pagination20
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    # def create(self, request, *args, **kwargs):
    #     ser = ModuleCreateUpdateSerializer(data=request.data)
    #     ser.is_valid(raise_exception=True)
    #
    #     Module.objects.create(name=ser.data['name'])
    #
    #     return Response(data={'error_code': 0,
    #                           'data': ser.data},
    #                     status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
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

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(data={'error_code': 0,
    #                           'data': serializer.data},
    #                     status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     self.serializer_class = ModuleCreateUpdateSerializer
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #
    #     serializer = self.get_serializer(instance, data=request.data,
    #                                      partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(data={'error_code': 0,
    #                           'data': serializer.data},
    #                     status=status.HTTP_200_OK)

    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #     except Exception:
    #         return Response(data={'error_code': 0,
    #                               'data': {}},
    #                         status=status.HTTP_200_OK)
    #
    #     instance.is_deleted = True
    #     instance.save()
    #     return Response(data={'error_code': 0,
    #                           'data': {}},
    #                     status=status.HTTP_200_OK)


class ModulePlatformsView(APIView):
    http_method_names = ('get',)

    def get(self, request):
        """
        拼凑出module/platform的依赖关系组合列表
        :param request:
        :return:
        """
        q = request.GET.get('q', '')
        modules = Module.objects.filter(
            is_deleted=False).select_related('platform')
        res_list = []
        for m in modules:
            if q in m.name or q in m.platform.name:
                res_list.append({
                    'id': '{}/{}'.format(m.id, m.platform_id),
                    'name': '{}/{}'.format(m.name, m.platform.name)
                })
        return Response(data={'error_code': 0,
                              'data': res_list},
                        status=status.HTTP_200_OK)


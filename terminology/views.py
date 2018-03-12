# coding=utf-8
from django.db import IntegrityError
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.paginations import Pagination20
from terminology.models import Terminology
from terminology.serializers import TerminologySerializer, \
    TerminologyListSerializer, TerminologyCreateSerializer, \
    TerminologyRetrieveSerializer, TerminologyUpdateSerializer


class TerminologyView(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    词库管理CRUD
    """
    queryset = Terminology.objects.filter(is_deleted=False)
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

        ser_data = ser.data['cla']

        queryset = self.queryset.filter(classification=ser_data)

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



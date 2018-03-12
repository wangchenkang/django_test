# coding=utf-8
from django.db import IntegrityError
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.paginations import Pagination20
from problem_classification.models import ProblemCla
from problem_classification.serializers import ProblemClaSerializer, \
    ProblemClaCreateSerializer, ProblemClaUpdateSerializer, \
    ProblemClaRetrieveSerializer


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

    def create(self, request, *args, **kwargs):
        ser = ProblemClaCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        ProblemCla.objects.create(name=ser.data['name'])

        return Response(data={'error_code': 0,
                              'data': ser.data},
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

        serializer = self.get_serializer(instance)
        return Response(data={'error_code': 0,
                              'data': serializer.data},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ProblemClaUpdateSerializer
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

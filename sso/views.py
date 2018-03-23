# coding=utf-8
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from common.paginations import Pagination20
from sso.models import PermissionsUser
from sso.serializers import SsoSerializer, SsoRetrieveSerializer


class SearchView(GenericAPIView):
    http_method_names = ['get']
    serializer_class = SsoRetrieveSerializer
    pagination_class = Pagination20

    def get(self, request):
        # 用户绑定角色时使用，让用户可选
        ser = SsoSerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)

        queryset = PermissionsUser.objects.using('sso').filter(
            name__icontains=ser.data['name']).order_by('id')

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



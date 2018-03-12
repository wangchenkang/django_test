# coding=utf-8
from django.db import IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException, \
    NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.db.models import ObjectDoesNotExist


def custom_exception_handler(e, context):

    if isinstance(e, ValidationError):
        # status.HTTP_406_NOT_ACCEPTABLE
        return Response(data={'error_code': 4,
                              # 'msg': e.detail,
                              'msg': '406 传参验证未通过',
                              'data': {}},
                        status=status.HTTP_200_OK,)

    elif isinstance(e, IntegrityError):
        # status.HTTP_409_CONFLICT
        return Response(data={'error_code': 4,
                              'msg': '409 数据库已存在',
                              'data': {}},
                        status=status.HTTP_200_OK)

    elif isinstance(e, Http404):
        # status.HTTP_404_NOT_FOUND
        return Response(data={'error_code': 4,
                              # 'msg': e.args[0],
                              'msg': '404 未找到',
                              'data': {}},
                        status=status.HTTP_200_OK)

    elif isinstance(e, NotAuthenticated):
        return Response(data={'error_code': 1,
                              'msg': '请登录后尝试',
                              'data': {}},
                        status=status.HTTP_200_OK)

    elif isinstance(e, PermissionDenied):
        return Response(data={'error_code': 2,
                              'msg': 'csrf token不正确',
                              'data': {}},
                        status=status.HTTP_200_OK)

    else:
        response = exception_handler(e, context)

        return response



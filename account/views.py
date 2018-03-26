# coding=utf-8
import hashlib

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser, User, Group
from django.db import IntegrityError, transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Role
from account.serializers import AccountSerializer, RoleSerializer, \
    RoleCreateSerializer, AccountCreateSerializer, AccountUpdateSerializer, \
    RoleRetrieveSerializer
from common.paginations import Pagination20
from sso.models import PermissionsUser
from terminology.models import Terminology
from terminology.serializers import TerminologySerializer, \
    TerminologyListSerializer, TerminologyCreateSerializer, \
    TerminologyRetrieveSerializer, TerminologyUpdateSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.middleware import SessionMiddleware
from rest_framework.authentication import SessionAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from django.middleware.security import SecurityMiddleware
from django.middleware.common import CommonMiddleware


class TestView(APIView):
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def post(self, request):
        return Response(data={'msg': 'test'}, status=status.HTTP_200_OK)


class LoginView(APIView):
    http_method_names = ['post']

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        if isinstance(request.user, AnonymousUser):
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                password_md5 = hashlib.md5(password.encode()).hexdigest()
                try:
                    sso = PermissionsUser.objects.using('sso').get(
                        name=username, pwd=password_md5)
                except PermissionsUser.DoesNotExist:
                    return Response(data={'error_code': 1,
                                          'msg': '用户名或密码不正确',
                                          'data': {}},
                                    status=status.HTTP_200_OK)
                else:
                    user, create = User.objects.get_or_create(username=sso.name)
                    user.set_password(password)
                    user.first_name = sso.id
                    user.save()
                    login(request, user)

        instance = Role.objects.filter(
            is_deleted=False,
            groups__in=request.user.groups.values_list('id', flat=True)
        ).order_by('id')

        if len(instance):
            ser = RoleRetrieveSerializer(instance[0])
            data = ser.data
        else:
            data = {}

        return Response(data={'error_code': 0,
                              'data': data},
                        status=status.HTTP_200_OK)


class LogoutView(APIView):
    http_method_names = ['get']

    def get(self, request):
        logout(request)
        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)


class AccountView(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    user
    """
    queryset = User.objects.filter(is_active=True).order_by('id')
    serializer_class = AccountSerializer
    pagination_class = Pagination20
    # :todo 加上
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        ser = AccountCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        try:
            sso = PermissionsUser.objects.using('sso').get(
                name=ser.data['username'])
        except PermissionsUser.DoesNotExist:
            raise ValidationError('sso中没有这个用户')

        with transaction.atomic():
            user = User.objects.create(
                username=ser.data['username'],
                first_name=sso.id,
            )
            user.groups.add(*ser.data['groups'])

        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

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
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(data={'error_code': 0,
                              'data': serializer.data},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        ser = AccountUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        instance = self.get_object()

        with transaction.atomic():
            instance.groups.clear()
            instance.groups.add(*ser.data['groups'])
            # Group.objects.filter(role=instance).update(
            #     name=ser.data['name'])
            # instance.save()

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

        instance.is_active = False
        instance.save()
        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)


class RoleView(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    """
    角色管理CRUD
    """
    queryset = Role.objects.filter(is_deleted=False).order_by('id')
    serializer_class = RoleSerializer
    pagination_class = Pagination20
    # :todo 加上
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        ser = RoleCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        with transaction.atomic():
            g = Group.objects.create(name=ser.data['name'])
            Role.objects.create(
                groups=g,
                has_data_display=ser.data['has_data_display'],
                has_classification=ser.data['has_classification'],
                has_problem=ser.data['has_problem'],
                has_terminology=ser.data['has_terminology'],
                has_user=ser.data['has_user'],
                has_role=ser.data['has_role'],
            )

        return Response(data={'error_code': 0,
                              'data': ser.data},
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

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
        instance = self.get_object()

        self.serializer_class = RoleRetrieveSerializer
        ser = self.get_serializer(instance, data=request.data)
        ser.is_valid(raise_exception=True)

        return Response(data={'error_code': 0,
                              'data': ser.data},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        ser = RoleCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        instance = self.get_object()

        with transaction.atomic():
            try:
                g = Group.objects.get(name=ser.data.get('name', ''))
            except Group.DoesNotExist:
                pass
            else:
                if g.id != instance.groups.id:
                    raise ValidationError
            instance.groups.name = ser.data['name']
            instance.has_data_display = ser.data['has_data_display']
            instance.has_classification = ser.data['has_classification']
            instance.has_problem = ser.data['has_problem']
            instance.has_terminology = ser.data['has_terminology']
            instance.has_user = ser.data['has_user']
            instance.has_role = ser.data['has_role']
            instance.groups.save()
            instance.save()

        return Response(data={'error_code': 0,
                              'data': ser.data},
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

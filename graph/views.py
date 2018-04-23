# coding=utf-8
import json
import operator
from functools import reduce

from django.db import IntegrityError, transaction, models
from rest_framework import mixins, viewsets, status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from graph.models import FrontendLayout
from graph.serializers import GraphQuerySerializer
from graph.utils import *
from problem.models import Problem, UserInJira, UniversityInJira
from problem_classification.models import ProblemCla
from terminology.models import Platform


class GraphView(APIView):
    http_method_names = ('get',)
    queryset = Problem.objects.filter(is_deleted=False)

    def get(self, request):
        slice_id = request.query_params.get('slice_id', 1)  # 表示是哪个图

        try:
            _slice = FrontendLayout.objects.get(pk=slice_id)
        except FrontendLayout.DoesNotExist:
            return Response(data={'error_code': 4, 'error_msg': '未找到'},
                            status=status.HTTP_404_NOT_FOUND)

        query = globals().get('slice_{}'.format(slice_id))

        # 搜索
        ser = GraphQuerySerializer(data=json.loads(request.query_params.get('filters')))
        ser.is_valid(raise_exception=True)
        query_list = []
        for k, v in ser.data.items():
            if 'time' in k:
                v = json.loads(v)
            [(k2, v2)] = v[0].items()
            if v2:
                query_list.append(models.Q(**{k2: v2}))

        if len(query_list) == 1:
            queries = query_list[0]
        elif len(query_list) > 1:
            queries = reduce(operator.and_, query_list)
        else:
            queries = models.Q()

        # print(self.queryset.filter(queries).query)
        self.queryset = self.queryset.filter(queries)

        res = query(self.queryset, _slice)

        return Response(data={'error_code': 0,
                              'error_msg': '',
                              'data': res},
                        status=status.HTTP_200_OK)


        p_total_count = self.queryset.count()

        aa = xx('p_clf_count', '问题类别数量', '类', p_total_count)

        p_total_count = x_number('p_clf_count', '问题类别数量', '类', p_total_count)

        p_clf_list = self.queryset.values('classification__name').annotate(p_count=Count('classification'))

        p_clf_count = p_clf_list.count()

        x_pie_list = []
        for clf in p_clf_list:
            x_pie_list.append(clf)

        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT count(*) as count
FROM (
  SELECT problem_cla.name, count(problem.classification_id) as count
  FROM problem
  JOIN problem_cla ON problem.classification_id = problem_cla.id
  GROUP BY problem.classification_id
) as _
            """)

            print(cursor.fetchone())
            for i in cursor.fetchall():
                print(i)

        queryset = self.queryset.values('classification__name').annotate(p_count=Count('classification')).query


        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)


class GraphLayoutView(APIView):
    http_method_names = ('get',)

    def get(self, request):
        # 加载页面图表布局
        page_id = int(request.query_params.get('page_id', 0))  # 表示是哪个dashboard

        fls = FrontendLayout.objects.filter(page=page_id).values(
            'id', 'x', 'y', 'w', 'h', 'width', 'height', 'i', 'chart_type',
            'title', 'component'
        )
        slice_list = []
        for fl in fls:
            slice_list.append(fl)

        return Response(data={'error_code': 0,
                              'error_msg': '',
                              'data': {'slices': slice_list}},
                        status=status.HTTP_200_OK)


class GraphSearchJiraCodeView(APIView):
    http_method_names = ('get',)

    def get(self, request):
        # 根据jira_code模糊匹配
        q = request.query_params.get('q', '')
        data = Problem.objects.filter(
            is_deleted=False, jira_code__icontains=q).extra(
            select={'name': 'jira_code'}).values('id', 'name')

        return Response(data={'error_code': 0,
                              'data': data},
                        status=status.HTTP_200_OK)


class GraphSearchClassificationView(APIView):
    http_method_names = ('get',)

    def get(self, request):
        # 根据classification模糊匹配
        q = request.query_params.get('q', '')
        data = ProblemCla.objects.filter(
            is_deleted=False, is_active=True,
            name__contains=q).values('id', 'name')

        return Response(data={'error_code': 0,
                              'data': data},
                        status=status.HTTP_200_OK)


class GraphSearchPlatformView(APIView):
    http_method_names = ('get',)

    def get(self, request):
        # 根据platform模糊匹配
        q = request.query_params.get('q', '')
        data = Platform.objects.filter(
            is_deleted=False, name__contains=q).values('id', 'name')

        return Response(data={'error_code': 0,
                              'data': data},
                        status=status.HTTP_200_OK)


class GraphSearchUserInJiraView(APIView):
    http_method_names = ('get',)

    def get(self, request):
        # 根据user_in_jira模糊匹配
        q = request.query_params.get('q', '')
        data = UserInJira.objects.filter(username__contains=q).extra(
            select={'name': 'username'}).values('id', 'name')

        return Response(data={'error_code': 0,
                              'data': data},
                        status=status.HTTP_200_OK)


class GraphSearchUniversityView(APIView):
    http_method_names = ('get',)

    def get(self, request):
        # 根据university模糊匹配
        q = request.query_params.get('q', '')
        data = UniversityInJira.objects.filter(name__contains=q).values(
            'id', 'name')

        return Response(data={'error_code': 0,
                              'data': data},
                        status=status.HTTP_200_OK)


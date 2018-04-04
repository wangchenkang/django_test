# coding=utf-8
import io
import os
import zipfile
import requests
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from rest_framework import status, mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from common.storage import Storage
from django.conf import settings
from script.models import Script


class UploadView(APIView):
    http_method_names = ['post']

    def post(self, request):
        """
        上传执行脚本，支持批量上传，通过id的key判断是更新脚本还是新建脚本
        :param request:
        :return:
        """
        files = request.FILES.getlist('scripts')

        script_id = request.data.get('id', None)

        script_name_set = set()
        if script_id:
            script = Script.objects.get(pk=script_id, is_deleted=False)
            folder_name = os.path.basename(script.path)
            script_name_set = set(script.name.split(','))
        else:
            folder_name = get_random_string(length=32)

        storage = Storage()
        files.append(open('{}/web/__init__.py'.format(settings.BASE_DIR), 'r'))

        file_list = []
        for f in files:
            res, url = storage.upload(
                '/{}/{}/'.format(
                    settings.STATIC_SERVER['FOLDER'], folder_name), f)

            filename = os.path.split(f.name)[1]
            script_name_set.add(filename)

            if res:
                file_list.append({
                    'file_name': filename,
                    'status': 0,  # '上传成功'
                })
            else:
                file_list.append({
                    'file_name': filename,
                    'status': 1,  # '上传失败'
                })

        success_file_list = list(filter(lambda x: x['status'] == 0, file_list))

        # print(list(success_file_list))

        if not script_id:
            script = Script.objects.create(
                name=','.join([i['file_name'] for i in success_file_list]),
                path='{}/{}/{}/'.format(
                    settings.STATIC_SERVER['PATH_PREFIX'],
                    settings.STATIC_SERVER['FOLDER'],
                    folder_name),
                run_command='',
                count=len(success_file_list),
            )
        else:
            script.name = ','.join(script_name_set)
            script.count = len(script_name_set)
            script.save()

        return Response(data={'error_code': 0,
                              'data': {
                                  'files': file_list,
                                  'id': script.id,
                              }},
                        status=status.HTTP_200_OK)


class ScriptView(GenericAPIView):

    http_method_names = ('get',)
    queryset = Script.objects.filter(is_deleted=False)

    def get(self, request, pk):
        """
        列出脚本的name
        :param request:
        :param pk:
        :return:
        """
        instance = self.get_object()

        return Response(data={'error_code': 0,
                              'data': {
                                  'name': instance.name.split(',')
                              }},
                        status=status.HTTP_200_OK)


class DownloadView(GenericAPIView):

    http_method_names = ('get',)
    queryset = Script.objects.filter(is_deleted=False)

    def get(self, request, pk):
        """
        下载脚本，支持下载指定脚本
        :param request:
        :param pk:
        :return:
        """
        script = self.get_object()
        folder_name = os.path.basename(script.path[:-1])

        single_file = request.query_params.get('name', None)

        name_list = script.name.split(',')

        if len(name_list) == 1:
            single_file = name_list[0]

        temp = []
        if single_file:
            url = '{}/{}/{}/{}'.format(
                settings.STATIC_SERVER['PUBLIC_HOST'],
                settings.STATIC_SERVER['FOLDER'],
                folder_name,
                single_file
            )
            res = requests.get(url)

            response = HttpResponse(res.text)
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename={}'.format(
                single_file
            )
        else:
            buff = io.BytesIO()
            zip_archive = zipfile.ZipFile(buff, 'w')

            for i, s in enumerate(name_list):
                url = '{}/{}/{}/{}'.format(
                    settings.STATIC_SERVER['PUBLIC_HOST'],
                    settings.STATIC_SERVER['FOLDER'],
                    folder_name,
                    s
                )

                res = requests.get(url)
                temp.append(io.BytesIO())
                temp[i].write(res.content)

                zip_archive.writestr(s, temp[i].getvalue())

            zip_archive.close()
            # print(zip_archive.printdir())

            response = HttpResponse(buff.getvalue())
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename={}.zip' \
                                              ''.format(folder_name)

        return response


class DeleteView(mixins.DestroyModelMixin, viewsets.GenericViewSet):

    queryset = Script.objects.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return Response(data={'error_code': 0,
                                  'data': {}},
                            status=status.HTTP_200_OK)
        file_name = request.data.get('file_name', '')
        name_list = instance.name.split(',')

        if name_list:
            try:
                name_list.remove(file_name)
            except KeyError:
                pass

            if len(name_list) == 0:
                instance.is_deleted = True

            instance.name = ','.join(name_list)
            instance.count -= 1
            instance.save()

        return Response(data={'error_code': 0,
                              'data': {}},
                        status=status.HTTP_200_OK)
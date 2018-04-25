# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import loader, Template, Context


# class EntryView(TemplateView):
#     """
#     就是为了加载导航页，其他不做
#     """
#     template_name = 'entry/index.html'


# def entry(request):
#     return render(request, 'entry/index.html')


# def entry(request):
#     t = loader.get_template('entry/index.html')
#     return HttpResponse(t.render())


def entry(request):
    """
    上面三个都是可以的，但应该都是启动时加到了内存中，
    现在这种我是不推荐用的，不过访问量小应该没啥问题，
    使用这种方式是为了前端更新代码时不用重启后端服务
    :param request:
    :return:
    """
    f = open('/opt/app/hunting-tracker-fe/dist/index.html')
    template = Template(f.read())
    f.close()
    return HttpResponse(template.render(Context({})))

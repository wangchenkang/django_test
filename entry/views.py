# coding=utf-8
from django.shortcuts import render
from django.views.generic import TemplateView


# class EntryView(LoginDispatchMixin, TemplateView):
class EntryView(TemplateView):
    """
    就是为了加载导航页，其他不做
    """
    template_name = 'entry/index.html'

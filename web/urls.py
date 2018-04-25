"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from entry.views import entry


urlpatterns = [
    # url(r'^$', EntryView.as_view(), name='entry'),
    url(r'^$', entry, name='entry'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^sso/', include('sso.urls', namespace='sso')),
    url(r'^terminology/', include('terminology.urls', namespace='terminology')),
    url(r'^problem_cla/', include('problem_classification.urls',
                                  namespace='problem_cla')),
    url(r'^problem/', include('problem.urls', namespace='problem')),
    url(r'^cycle_task/', include('cycle_task.urls', namespace='cycle_task')),
    url(r'^graph/', include('graph.urls', namespace='graph')),
    url(r'^script/', include('script.urls', namespace='script')),
]

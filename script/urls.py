from django.conf.urls import url, include
from rest_framework import routers

from script.views import ScriptView, UploadView, DownloadView, DeleteView

delete_router = routers.SimpleRouter()
delete_router.register(r'', DeleteView)

urlpatterns = [
    url(r'^(?P<pk>[\d]+)/$', ScriptView.as_view(), name='scripts'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^download/(?P<pk>[\d]+)/$', DownloadView.as_view(), name='download'),
    url(r'^delete/', include(delete_router.urls, namespace='delete')),
]

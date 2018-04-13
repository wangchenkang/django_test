from django.conf.urls import url, include
from rest_framework import routers

from terminology.views import TerminologyView, PlatformView, ModuleView, \
    ModulePlatformsView


# 先隐掉
# terminology_router = routers.SimpleRouter()
# terminology_router.register(r't', TerminologyView)
platform_router = routers.SimpleRouter()
platform_router.register(r'platform', PlatformView)
module_router = routers.SimpleRouter()
module_router.register(r'module', ModuleView)


urlpatterns = [
    # url(r'', include(terminology_router.urls, namespace='terminology')),
    url(r'^module_platforms/$', ModulePlatformsView.as_view(),
        name='module_platforms'),
    url(r'', include(platform_router.urls, namespace='platform')),
    url(r'', include(module_router.urls, namespace='module')),
]

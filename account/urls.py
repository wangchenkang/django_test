from django.conf.urls import url, include
from rest_framework import routers

from account.views import LoginView, LogoutView, AccountView, RoleView, \
    TestView

account_router = routers.SimpleRouter()
account_router.register(r'', AccountView)

role_router = routers.SimpleRouter()
role_router.register(r'', RoleView)

urlpatterns = [
    url(r'^test/$', TestView.as_view(), name='test'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^role/', include(role_router.urls, namespace='role')),
    url(r'^', include(account_router.urls, namespace='account')),
]

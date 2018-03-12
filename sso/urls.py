from django.conf.urls import url

from sso.views import SearchView


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='sso_search'),
]

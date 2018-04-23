from django.conf.urls import url

from graph.views import GraphView, GraphLayoutView, GraphSearchJiraCodeView, \
    GraphSearchClassificationView, GraphSearchPlatformView, \
    GraphSearchUserInJiraView, GraphSearchUniversityView

urlpatterns = [
    url(r'^slice/$', GraphView.as_view(), name='slice'),
    url(r'^layout/$', GraphLayoutView.as_view(), name='layout'),

    # 搜索条件相关
    url(r'^search/jira_code/$', GraphSearchJiraCodeView.as_view(),
        name='jira_code'),
    url(r'^search/clf/$', GraphSearchClassificationView.as_view(),
        name='classification'),
    url(r'^search/platform/$', GraphSearchPlatformView.as_view(),
        name='platform'),
    url(r'^search/user_in_jira/$', GraphSearchUserInJiraView.as_view(),
        name='user_in_jira'),
    url(r'^search/university/$', GraphSearchUniversityView.as_view(),
        name='university'),
]

from django.conf.urls import url, include
from rest_framework import routers

from cycle_task.views import CycleTaskView, AvailableProblemClaView,\
    TestView, CycleTaskResultView


cycle_task_router = routers.SimpleRouter()
cycle_task_router.register(r'', CycleTaskView)


urlpatterns = [
    url(r'^test/$', TestView.as_view(), name='test'),
    url(r'^send_result/$', CycleTaskResultView.as_view(), name='send_result'),
    url(r'^problem_cla/$', AvailableProblemClaView.as_view(),
        name='available_problem_cla'),
    url(r'', include(cycle_task_router.urls, namespace='cycle_task')),
]

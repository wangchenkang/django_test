from django.conf.urls import url, include
from rest_framework import routers

from cycle_task.views import CycleTaskView, AvailableProblemClaView


cycle_task_router = routers.SimpleRouter()
cycle_task_router.register(r'', CycleTaskView)


urlpatterns = [
    url(r'^problem_cla/$', AvailableProblemClaView.as_view(),
        name='available_problem_cla'),
    url(r'', include(cycle_task_router.urls, namespace='cycle_task')),
]

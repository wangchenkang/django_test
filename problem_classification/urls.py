from django.conf.urls import url, include
from rest_framework import routers

from problem_classification.views import ProblemClaView


problem_cla_router = routers.SimpleRouter()
problem_cla_router.register(r'', ProblemClaView)


urlpatterns = [
    url(r'^', include(problem_cla_router.urls, namespace='problem_cla')),
]

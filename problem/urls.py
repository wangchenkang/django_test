from django.conf.urls import url, include
from rest_framework import routers
from problem.views import ProblemView, Platform2Module


problem_router = routers.SimpleRouter()
problem_router.register(r'', ProblemView)


urlpatterns = [
    url(r'^platform2module/$', Platform2Module.as_view(),
        name='platform2module'),
    url(r'', include(problem_router.urls, namespace='problem')),
]

from django.conf.urls import url, include
from rest_framework import routers

from terminology.views import TerminologyView


terminology_router = routers.SimpleRouter()
terminology_router.register(r'', TerminologyView)


urlpatterns = [
    url(r'^', include(terminology_router.urls, namespace='terminology')),
    # url(r'',
    #     include([
    #         # url(r'^org/$',
    #         #     TeacherOrgView.as_view(),
    #         #     name="org"),
    #         # url(r'^bind/$',
    #         #     TeacherBindCourse.as_view(),
    #         #     name="teacher_bind_course"),
    #         # url(r'^(?P<course_id>[^/.]+)/bind/$',
    #         #     TeacherBindCourse.as_view(),
    #         #     name="course_teachers"),
    #         # url(r'^(?P<course_id>[^/.]+)/bind/(?P<tid>\d+)/$',
    #         #     TeacherBindCourse.as_view(),
    #         #     name="teacher_bind_course"),
    #
    #             ] + terminology_router.urls,
    #             namespace="terminology")),
]

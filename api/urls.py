from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('schools', views.SchoolViewSet, basename='school')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include([
        path('student/login/', views.student_login, name='student_login'),
        path('session', views.check_session, name='check_session'),
    ])),
]
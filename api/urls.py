from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'schools', views.SchoolViewSet)
router.register(r'students', views.StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/student/login/', views.student_login, name='student_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
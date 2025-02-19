from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('admin/', views.index, name='admin_dashboard'),
    path('guru/', views.guru_dashboard, name='guru_dashboard'),
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Pages Dashboard Admin
    # Student Management
    path('admin/students/', views.student_list, name='student_list'),
    path('admin/students/add/', views.add_student, name='add_student'),
    path('admin/students/delete/<uuid:student_id>/', views.delete_student, name='delete_student'),
    path('admin/students/get/<uuid:student_id>/', views.get_student, name='get_student'),
    path('admin/students/edit/<uuid:student_id>/', views.edit_student, name='edit_student'),
]
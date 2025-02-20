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
    path('admin/students/edit/<uuid:student_id>/', views.edit_student, name='edit_student'),

    # School Management
    path('admin/schools/', views.school_list, name='school_list'),
    path('admin/schools/add/', views.add_school, name='add_school'),
    path('admin/schools/edit/<uuid:school_id>/', views.edit_school, name='edit_school'),
    path('admin/schools/delete/<uuid:school_id>/', views.delete_school, name='delete_school'),

    # Attendance Management
    path('admin/attendance/', views.attendance_list, name='attendance_list'),
]
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
    # User Management
    path('admin/users/', views.user_list, name='user_list'),
    path('admin/users/add/', views.user_add, name='user_add'),
    path('admin/users/edit/<uuid:user_id>/', views.user_edit, name='user_edit'),
    path('admin/users/delete/<uuid:user_id>/', views.user_delete, name='user_delete'),
    # Student Management
    path('admin/students/', views.student_list, name='student_list'),
    path('admin/students/add/', views.add_student, name='add_student'),
    path('admin/students/delete/<uuid:student_id>/', views.delete_student, name='delete_student'),
    path('admin/students/edit/<uuid:student_id>/', views.edit_student, name='edit_student'),

    # School Management
    path('admin/schools/', views.school_list, name='school_list'),
    path('admin/schools/<uuid:school_id>/students/', views.school_students, name='school_students'),
    path('admin/schools/add/', views.add_school, name='add_school'),
    path('admin/schools/edit/<uuid:school_id>/', views.edit_school, name='edit_school'),
    path('admin/schools/delete/<uuid:school_id>/', views.delete_school, name='delete_school'),

    # Attendance Management
    path('admin/attendance/', views.attendance_list, name='attendance_list'),

    # Pages Dashboard Guru
    path('guru/students/', views.guru_student_list, name='guru_student_list'),
    path('guru/students/add/', views.guru_student_add, name='guru_student_add'),
    path('guru/students/edit/<uuid:student_id>/', views.guru_student_edit, name='guru_student_edit'),
    path('guru/students/delete/<uuid:student_id>/', views.guru_student_delete, name='guru_student_delete'),

    path('guru/attendance/', views.guru_attendance_list, name='guru_attendance_list'),
    path('guru/attendance/add/', views.guru_attendance_add, name='guru_attendance_add'),
    path('guru/attendance/edit/<uuid:attendance_id>/', views.guru_attendance_edit, name='guru_attendance_edit'),
    path('guru/attendance/delete/<uuid:attendance_id>/', views.guru_attendance_delete, name='guru_attendance_delete'),

    path('guru/permissions/', views.guru_permission_list, name='guru_permission_list'),
    path('guru/permissions/<uuid:permission_id>/update-status/', views.guru_permission_update_status, name='guru_permission_update_status'),
]
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_dashboard(request):
    return redirect('admin_dashboard')

urlpatterns = [
    path('', redirect_to_dashboard, name='home'),  # Add this line
    path('dashboard/', include('Dashboard.urls')),
    path('api/', include('api.urls')),
]
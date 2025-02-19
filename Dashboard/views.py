from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import Student
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Dashboards
@login_required
def index(request):
    return render(request, 'dashboard/admin_dashboard.html')

@login_required
def guru_dashboard(request):
    if request.user.role != 'GURU':
        return redirect('home')
        
    school = request.user.sekolah.first() if hasattr(request.user, 'sekolah') else None
    
    context = {
        'school': school
    }
    return render(request, 'dashboard/guru_dashboard.html', context)


# Auth
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.status_aktif:
                login(request, user)
                if user.role == 'ADMIN':
                    return redirect('admin_dashboard')
                elif user.role == 'GURU':
                    return redirect('guru_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# Pages Dashboard Admin

# Student Management
@login_required
def student_list(request):
    students = Student.objects.all().order_by('nama_lengkap')
    context = {
        'students': students,
    }
    return render(request, 'pages/student_list.html', context)

@login_required
def add_student(request):
    if request.method == 'POST':
        try:
            student = Student.objects.create(
                nisn=request.POST['nisn'],
                nama_lengkap=request.POST['nama_lengkap'],
                email=request.POST['email'],
                password=make_password(request.POST['password']),
                jenis_kelamin=request.POST['jenis_kelamin'],
                nomor_whatsapp=request.POST['nomor_whatsapp'],
                tinggi_badan=request.POST['tinggi_badan'],
                berat_badan=request.POST['berat_badan'],
                golongan_darah=request.POST['golongan_darah'],
                status_siswa=request.POST['status_siswa'],
                status_aktif=True
            )
            messages.success(request, 'Student added successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('student_list')

@login_required
def delete_student(request, student_id):
    if request.method == 'POST':
        try:
            student = get_object_or_404(Student, id=student_id)
            student.delete()
            messages.success(request, 'Student deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting student: {str(e)}')
    return redirect('student_list')

@login_required
@require_http_methods(["GET"])
def get_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    data = {
        'id': str(student.id),
        'nisn': student.nisn,
        'nama_lengkap': student.nama_lengkap,
        'email': student.email,
        'nomor_whatsapp': student.nomor_whatsapp,
        'jenis_kelamin': student.jenis_kelamin,
        'tinggi_badan': student.tinggi_badan,
        'berat_badan': student.berat_badan,
        'golongan_darah': student.golongan_darah,
        'status_siswa': student.status_siswa
    }
    return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
def edit_student(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        student.nisn = request.POST.get('nisn')
        student.nama_lengkap = request.POST.get('nama_lengkap')
        student.email = request.POST.get('email')
        student.nomor_whatsapp = request.POST.get('nomor_whatsapp')
        student.jenis_kelamin = request.POST.get('jenis_kelamin')
        student.tinggi_badan = request.POST.get('tinggi_badan')
        student.berat_badan = request.POST.get('berat_badan')
        student.golongan_darah = request.POST.get('golongan_darah')
        student.status_siswa = request.POST.get('status_siswa')
        
        print(f"Before saving: {student.__dict__}")  # Log student data before saving
        
        student.save()
        
        print(f"After saving: {student.__dict__}")  # Log student data after saving
        
        return JsonResponse({
            'status': 'success',
            'message': 'Student updated successfully'
        })
    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Log any exceptions that occur
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

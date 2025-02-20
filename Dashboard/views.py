from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import Student,School,User, Attendance
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Dashboards
@login_required
def index(request):
    context = {
        'segment': 'dashboard'
    }
    return render(request, 'dashboard/admin_dashboard.html',context)

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
    schools = School.objects.all()  # Add this line
    context = {
        'students': students,
        'schools': schools, 
        'segment': 'students',
        'breadcrumb': {
            'parent': 'Siswa',
            'child': 'Daftar Siswa'
        }
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
                sekolah_id=request.POST['sekolah'],
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
def edit_student(request, student_id):
    if request.method == 'GET':
        try:
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
                'status_siswa': student.status_siswa,
                'sekolah': str(student.sekolah.id) if student.sekolah else ''  # Change this line
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'POST':
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
            student.sekolah_id = request.POST.get('sekolah')
            student.save()
            messages.success(request, 'Student updated successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('student_list')

# School Management
@login_required
def school_list(request):
    schools = School.objects.all()
    teachers = User.objects.filter(role='GURU')
    context = {
        'schools': schools,
        'teachers': teachers,
        'title': 'Daftar Sekolah',
        'breadcrumb': {
            'parent': 'Sekolah',
            'child': 'Daftar Sekolah'
        }
    }
    return render(request, 'pages/school_list.html', context)

@login_required
def add_school(request):
    if request.method == 'POST':
        try:
            school = School.objects.create(
                npsn=request.POST['npsn'],
                nama_sekolah=request.POST['nama_sekolah'],
                alamat=request.POST['alamat'],
                kota=request.POST['kota'],
                provinsi=request.POST['provinsi'],
                kode_pos=request.POST['kode_pos'],
                telepon=request.POST['telepon'],
                email=request.POST['email'],
                website=request.POST['website'],
                kepala_sekolah=request.POST['kepala_sekolah'],
                guru_id=request.POST['guru'],
                status=request.POST['status']
            )
            messages.success(request, 'School added successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('school_list')

@login_required
def edit_school(request, school_id):
    if request.method == 'GET':
        try:
            school = get_object_or_404(School, id=school_id)
            data = {
                'id': str(school.id),
                'npsn': school.npsn,
                'nama_sekolah': school.nama_sekolah,
                'alamat': school.alamat,
                'kota': school.kota,
                'provinsi': school.provinsi,
                'kode_pos': school.kode_pos,
                'telepon': school.telepon,
                'email': school.email,
                'website': school.website,
                'kepala_sekolah': school.kepala_sekolah,
                'guru': str(school.guru_id) if school.guru_id else '',
                'status': school.status
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'POST':
        try:
            school = get_object_or_404(School, id=school_id)
            school.npsn = request.POST.get('npsn')
            school.nama_sekolah = request.POST.get('nama_sekolah')
            school.alamat = request.POST.get('alamat')
            school.kota = request.POST.get('kota')
            school.provinsi = request.POST.get('provinsi')
            school.kode_pos = request.POST.get('kode_pos')
            school.telepon = request.POST.get('telepon')
            school.email = request.POST.get('email')
            school.website = request.POST.get('website')
            school.kepala_sekolah = request.POST.get('kepala_sekolah')
            school.guru_id = request.POST.get('guru')
            school.status = request.POST.get('status')
            school.save()
            messages.success(request, 'School updated successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('school_list')

@login_required
def delete_school(request, school_id):
    if request.method == 'POST':
        try:
            school = get_object_or_404(School, id=school_id)
            school.delete()
            messages.success(request, 'School deleted successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('school_list')

# Attendance Management
@login_required
def attendance_list(request):
    attendances = Attendance.objects.select_related('student', 'sekolah').all().order_by('-date', '-time')
    schools = School.objects.all()
    context = {
        'attendances': attendances,
        'schools': schools,
        'title': 'Daftar Absensi',
        'breadcrumb': {
            'parent': 'Absensi',
            'child': 'Daftar Absensi'
        }
    }
    return render(request, 'pages/attendance.html', context)
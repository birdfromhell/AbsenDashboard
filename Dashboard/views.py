from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import Student,School,User, Attendance, AttendancePermission
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
import json

# Dashboards
@login_required
def index(request):
    # Get statistics
    total_schools = School.objects.filter(status='AKTIF').count()
    total_students = Student.objects.filter(status_siswa='AKTIF').count()
    total_teachers = User.objects.filter(role='GURU').count()
    total_attendance = Attendance.objects.filter(date=timezone.now().date()).count()
    
    # Get attendance percentage for today
    total_present = Attendance.objects.filter(
        date=timezone.now().date(),
        status='HADIR'
    ).count()
    
    attendance_percentage = (total_present / total_students * 100) if total_students > 0 else 0
    
    context = {
        'segment': 'dashboard',
        'total_schools': total_schools,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_attendance': total_attendance,
        'attendance_percentage': round(attendance_percentage, 2)
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


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


# User Management 
@login_required
def user_list(request):
    users = User.objects.all()
    context = {
        'users': users,
        'title': 'User Management',
        'breadcrumb': {
            'parent': 'Admin',
            'child': 'Users'
        }
    }
    return render(request, 'pages/user_list.html', context)

@login_required
def user_add(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                nama_lengkap=request.POST.get('nama_lengkap'),
                role=request.POST.get('role')
            )
            messages.success(request, 'User created successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('user_list')
@login_required
def user_list(request):
    users = User.objects.all()
    schools = School.objects.all()
    context = {
        'users': users,
        'schools': schools,
        'title': 'User Management',
        'breadcrumb': {
            'parent': 'Admin',
            'child': 'Users'  
        }
    }
    return render(request, 'pages/user_list.html', context)

@login_required 
def user_add(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'), 
                password=request.POST.get('password'),
                nama_lengkap=request.POST.get('nama_lengkap'),
                role=request.POST.get('role')
            )

            
            if user.role == 'GURU' and request.POST.get('sekolah'):
                school = School.objects.get(id=request.POST.get('sekolah'))
                school.guru = user
                school.save()

            messages.success(request, 'User created successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('user_list')

@login_required
def user_edit(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(User, id=user_id)
       
        school = School.objects.filter(guru=user).first()
        
        data = {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'nama_lengkap': user.nama_lengkap,
            'role': user.role,
            'status_aktif': user.status_aktif,
            'sekolah': str(school.id) if school else ''  
        }
        return JsonResponse(data)
        
    elif request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            old_role = user.role

            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.nama_lengkap = request.POST.get('nama_lengkap')
            user.role = request.POST.get('role')
            user.status_aktif = request.POST.get('status_aktif') == 'true'
            user.save()

            if user.role == 'GURU':
                if old_role != 'GURU':
                    School.objects.filter(guru=user).update(guru=None)
                
                if request.POST.get('sekolah'):
                    school = School.objects.get(id=request.POST.get('sekolah'))
                    school.guru = user
                    school.save()
            else:
                School.objects.filter(guru=user).update(guru=None)

            messages.success(request, 'User updated successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('user_list')

@login_required
def user_delete(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            
            if user.role == 'GURU':
                School.objects.filter(guru=user).update(guru=None)
                
            user.delete()
            messages.success(request, 'User deleted successfully')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('user_list')

# Student Management
@login_required
def student_list(request):
    students = Student.objects.all().order_by('nama_lengkap')
    schools = School.objects.all()
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
def school_students(request, school_id):
    try:
        school = get_object_or_404(School, id=school_id)
        students = Student.objects.filter(sekolah=school)
        
        data = {
            'school_name': school.nama_sekolah,
            'students': [{
                'nisn': student.nisn,
                'nama_lengkap': student.nama_lengkap,
                'email': student.email,
                'jenis_kelamin': student.jenis_kelamin,
                'status_siswa': student.status_siswa
            } for student in students]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
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


# Pages Guru Dashboard
@login_required
def guru_dashboard(request):
    if request.user.role != 'GURU':
        return redirect('admin_dashboard')
        
    school = School.objects.filter(guru=request.user).first()
    
    if school:
        total_students = Student.objects.filter(sekolah=school, status_siswa='AKTIF').count()
        today_attendance = Attendance.objects.filter(
            sekolah=school,
            date=timezone.now().date()
        ).count()
        

        total_present = Attendance.objects.filter(
            sekolah=school,
            date=timezone.now().date(),
            status='HADIR'
        ).count()
        
        attendance_percentage = (total_present / total_students * 100) if total_students > 0 else 0
        

        last_7_days = []
        attendance_data = []
        
        for i in range(6, -1, -1):
            date = timezone.now().date() - timezone.timedelta(days=i)
            total_day_students = Student.objects.filter(
                sekolah=school, 
                status_siswa='AKTIF'
            ).count()
            
            present_count = Attendance.objects.filter(
                sekolah=school,
                date=date,
                status='HADIR'
            ).count()
            
            percentage = (present_count / total_day_students * 100) if total_day_students > 0 else 0
            last_7_days.append(date.strftime('%a'))
            attendance_data.append(round(percentage))

        status_distribution = {
            'AKTIF': Student.objects.filter(sekolah=school, status_siswa='AKTIF').count(),
            'ALUMNI': Student.objects.filter(sekolah=school, status_siswa='ALUMNI').count(),
            'PINDAH': Student.objects.filter(sekolah=school, status_siswa='PINDAH').count(),
            'DIKELUARKAN': Student.objects.filter(sekolah=school, status_siswa='DIKELUARKAN').count()
        }
        today_attendance_counts = {
            'HADIR': Attendance.objects.filter(
                sekolah=school,
                date=timezone.now().date(),
                status='HADIR'
            ).count(),
            'SAKIT': Attendance.objects.filter(
                sekolah=school,
                date=timezone.now().date(),
                status='SAKIT'
            ).count(),
            'IZIN': Attendance.objects.filter(
                sekolah=school,
                date=timezone.now().date(),
                status='IZIN'
            ).count(),
            'ALPHA': Attendance.objects.filter(
                sekolah=school,
                date=timezone.now().date(),
                status='ALPHA'
            ).count()
        }
        
        context = {
            'segment': 'dashboard',
            'school': school,
            'total_students': total_students,
            'today_attendance': today_attendance,
            'attendance_percentage': round(attendance_percentage, 2),
            'last_7_days': last_7_days,
            'attendance_data': attendance_data,
            'status_distribution': status_distribution,
            'today_attendance_counts': today_attendance_counts
        }
        return render(request, 'dashboard/guru_dashboard.html', context)
    else:
        messages.error(request, 'Anda belum ditugaskan ke sekolah manapun')
        return redirect('login')
    
@login_required
def guru_student_list(request):
    if request.user.role != 'GURU':
        return redirect('student_list')
        
    school = School.objects.filter(guru=request.user).first()
    
    if school:
        students = Student.objects.filter(sekolah=school)
        context = {
            'students': students,
            'school': school,
            'title': 'Daftar Siswa',
            'breadcrumb': {
                'parent': 'Siswa',
                'child': 'Daftar Siswa'
            }
        }
        return render(request, 'pages/guru/student_list.html', context)
    else:
        messages.error(request, 'Anda belum ditugaskan ke sekolah manapun')
        return redirect('guru_dashboard')

@login_required
def guru_student_add(request):
    if request.user.role != 'GURU':
        return redirect('student_list')

    if request.method == 'POST':
        try:
            school = School.objects.filter(guru=request.user).first()
            if not school:
                raise Exception('Anda belum ditugaskan ke sekolah manapun')

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
                status_siswa='AKTIF',
                sekolah=school,
                status_aktif=True
            )
            messages.success(request, 'Siswa berhasil ditambahkan')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('guru_student_list')

@login_required
def guru_student_edit(request, student_id):
    if request.user.role != 'GURU':
        return redirect('student_list')

    school = School.objects.filter(guru=request.user).first()
    if not school:
        messages.error(request, 'Anda belum ditugaskan ke sekolah manapun')
        return redirect('guru_dashboard')

    if request.method == 'GET':
        try:
            student = get_object_or_404(Student, id=student_id, sekolah=school)
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'POST':
        try:
            student = get_object_or_404(Student, id=student_id, sekolah=school)
            student.nisn = request.POST.get('nisn')
            student.nama_lengkap = request.POST.get('nama_lengkap')
            student.email = request.POST.get('email')
            student.nomor_whatsapp = request.POST.get('nomor_whatsapp')
            student.jenis_kelamin = request.POST.get('jenis_kelamin')
            student.tinggi_badan = request.POST.get('tinggi_badan')
            student.berat_badan = request.POST.get('berat_badan')
            student.golongan_darah = request.POST.get('golongan_darah')
            student.status_siswa = request.POST.get('status_siswa')
            student.save()
            messages.success(request, 'Data siswa berhasil diperbarui')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('guru_student_list')

@login_required
def guru_student_delete(request, student_id):
    if request.user.role != 'GURU':
        return redirect('student_list')

    if request.method == 'POST':
        try:
            school = School.objects.filter(guru=request.user).first()
            if not school:
                raise Exception('Anda belum ditugaskan ke sekolah manapun')

            student = get_object_or_404(Student, id=student_id, sekolah=school)
            student.delete()
            messages.success(request, 'Siswa berhasil dihapus')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('guru_student_list')

@login_required
def guru_attendance_list(request):
    if request.user.role != 'GURU':
        return redirect('attendance_list')
        
    school = School.objects.filter(guru=request.user).first()
    
    if school:
        # Get all attendances for the teacher's school
        attendances = Attendance.objects.select_related('student', 'sekolah').filter(
            sekolah=school
        ).order_by('-date', '-time')
        
        students = Student.objects.filter(sekolah=school, status_siswa='AKTIF')
        
        context = {
            'attendances': attendances,
            'students': students,
            'school': school,
            'title': 'Daftar Absensi',
            'breadcrumb': {
                'parent': 'Absensi',
                'child': 'Daftar Absensi'
            }
        }
        return render(request, 'pages/guru/attendance_list.html', context)
    else:
        messages.error(request, 'Anda belum ditugaskan ke sekolah manapun')
        return redirect('guru_dashboard')

@login_required
def guru_attendance_add(request):
    if request.user.role != 'GURU':
        return redirect('attendance_list')

    if request.method == 'POST':
        try:
            school = School.objects.filter(guru=request.user).first()
            if not school:
                raise Exception('Anda belum ditugaskan ke sekolah manapun')

            attendance = Attendance.objects.create(
                student_id=request.POST['student'],
                sekolah=school,
                date=request.POST['date'],
                status=request.POST['status'],
                absen_type=request.POST['absen_type'],
                location=request.POST.get('location', ''),
                photo=request.FILES.get('photo', None)
            )
            messages.success(request, 'Absensi berhasil ditambahkan')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('guru_attendance_list')

@login_required
def guru_attendance_edit(request, attendance_id):
    if request.user.role != 'GURU':
        return redirect('attendance_list')

    school = School.objects.filter(guru=request.user).first()
    if not school:
        messages.error(request, 'Anda belum ditugaskan ke sekolah manapun')
        return redirect('guru_dashboard')

    if request.method == 'GET':
        try:
            attendance = get_object_or_404(Attendance, id=attendance_id, sekolah=school)
            data = {
                'id': str(attendance.id),
                'student': str(attendance.student.id),
                'date': attendance.date.strftime('%Y-%m-%d'),
                'time': attendance.time.strftime('%H:%M'),
                'status': attendance.status,
                'absen_type': attendance.absen_type,
                'location': attendance.location or '',
                'photo_url': attendance.photo.url if attendance.photo else ''
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'POST':
        try:
            attendance = get_object_or_404(Attendance, id=attendance_id, sekolah=school)
            attendance.student_id = request.POST.get('student')
            attendance.date = request.POST.get('date')
            attendance.status = request.POST.get('status')
            attendance.absen_type = request.POST.get('absen_type')
            attendance.location = request.POST.get('location', '')
            
            if 'photo' in request.FILES:
                attendance.photo = request.FILES['photo']
                
            attendance.save()
            messages.success(request, 'Data absensi berhasil diperbarui')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('guru_attendance_list')

@login_required
def guru_attendance_delete(request, attendance_id):
    if request.user.role != 'GURU':
        return redirect('attendance_list')

    if request.method == 'POST':
        try:
            school = School.objects.filter(guru=request.user).first()
            if not school:
                raise Exception('Anda belum ditugaskan ke sekolah manapun')

            attendance = get_object_or_404(Attendance, id=attendance_id, sekolah=school)
            attendance.delete()
            messages.success(request, 'Data absensi berhasil dihapus')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('guru_attendance_list')

@login_required
def guru_permission_list(request):
    if request.user.role != 'GURU':
        return redirect('admin_dashboard')
        
    school = School.objects.filter(guru=request.user).first()
    
    if school:
        pending_permissions_count = AttendancePermission.objects.filter(
            sekolah=school,
            accept_status='PENDING'
        ).count()
        
        permissions = AttendancePermission.objects.select_related('student').filter(
            sekolah=school
        ).order_by('-date')
        
        context = {
            'permissions': permissions,
            'school': school,
            'pending_permissions_count': pending_permissions_count,
            'title': 'Daftar Izin/Sakit',
            'breadcrumb': {
                'parent': 'Izin/Sakit',
                'child': 'Daftar'
            }
        }
        return render(request, 'pages/guru/permission_list.html', context)
    else:
        messages.error(request, 'Anda belum ditugaskan ke sekolah manapun')
        return redirect('guru_dashboard')

@login_required
def guru_permission_update_status(request, permission_id):
    if request.user.role != 'GURU':
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        try:
            school = School.objects.filter(guru=request.user).first()
            if not school:
                raise Exception('Anda belum ditugaskan ke sekolah manapun')
                
            permission = get_object_or_404(
                AttendancePermission, 
                id=permission_id,
                sekolah=school,
                accept_status='PENDING'
            )
            
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if new_status not in ['APPROVED', 'REJECTED']:
                raise Exception('Status tidak valid')
                
            permission.accept_status = new_status
            permission.save()
            
            return JsonResponse({'message': 'Status berhasil diperbarui'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)
from django.contrib.auth.hashers import make_password
from .models import User, Student, School, Attendance, AttendancePermission
import uuid
from django.utils import timezone
from datetime import datetime, timedelta
import random

def seed_users():
    users = [
        {
            'id': uuid.uuid4(),
            'username': 'admin',
            'email': 'admin@example.com',
            'password': make_password('admin123'),
            'role': 'ADMIN',
            'nama_lengkap': 'Administrator',
            'status_aktif': True
        },
        {
            'id': uuid.uuid4(),
            'username': 'guru1',
            'email': 'guru1@example.com', 
            'password': make_password('guru123'),
            'role': 'GURU',
            'nama_lengkap': 'Guru Satu',
            'status_aktif': True
        }
    ]

    created_count = 0
    for user_data in users:
        _, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            created_count += 1
    
    print(f"Users seeded successfully! ({created_count} new users created)")

def seed_students():
    students = [
        {
            'id': uuid.uuid4(),
            'nisn': '1234567890',
            'email': 'student1@example.com',
            'password': make_password('student123'),
            'nama_lengkap': 'f',
            'jenis_kelamin': 'L',
            'nomor_whatsapp': '081234567890',
            'tinggi_badan': 170,
            'berat_badan': 65,
            'golongan_darah': 'A',
            'status_siswa': 'AKTIF',
            'status_aktif': True
        },
        {
            'id': uuid.uuid4(),
            'nisn': '0987654321',
            'email': 'student2@example.com',
            'password': make_password('student123'),
            'nama_lengkap': 'Jane Doe',
            'jenis_kelamin': 'P',
            'nomor_whatsapp': '081234567891',
            'tinggi_badan': 165,
            'berat_badan': 55,
            'golongan_darah': 'B',
            'status_siswa': 'AKTIF',
            'status_aktif': True
        }
    ]

    created_count = 0
    for student_data in students:
        _, created = Student.objects.get_or_create(
            nisn=student_data['nisn'],
            defaults=student_data
        )
        if created:
            created_count += 1
    
    print(f"Students seeded successfully! ({created_count} new students created)")

def seed_schools():
    guru = User.objects.filter(role='GURU').first()
    
    schools = [
        {
            'id': uuid.uuid4(),
            'npsn': '10000001',
            'nama_sekolah': 'SMA Negeri 1',
            'alamat': 'Jl. Contoh No. 1',
            'kota': 'Jakarta',
            'provinsi': 'DKI Jakarta',
            'kode_pos': '12345',
            'email': 'sman1@example.com',
            'telepon': '021-1234567',
            'kepala_sekolah': 'Dr. John Doe',
            'guru': guru,
            'status': 'AKTIF'
        }
    ]
    
    created_count = 0
    for school_data in schools:
        School.objects.get_or_create(
        npsn=school_data['npsn'],
        defaults=school_data
        )
        if created_count:
            created_count += 1


def seed_attendance():
    students = Student.objects.filter(status_aktif=True)
    
    attendance_data = []
    today = timezone.now().date()
    
    for student in students:
        school = student.sekolah
        if school:
            for i in range(7):
                date = today - timedelta(days=i)
                attendance_data.append({
                    'id': uuid.uuid4(),
                    'student': student,
                    'sekolah': school,
                    'date': date,
                    'time': datetime.strptime('07:30', '%H:%M').time(),
                    'status': random.choice(['HADIR', 'ALPA']),
                    'absen_type': 'MASUK',
                    'location': 'Gerbang Sekolah',
                })
                
                attendance_data.append({
                    'id': uuid.uuid4(),
                    'student': student,
                    'sekolah': school,
                    'date': date,
                    'time': datetime.strptime('15:00', '%H:%M').time(),
                    'status': random.choice(['HADIR', 'ALPA']),
                    'absen_type': 'PULANG',
                    'location': 'Gerbang Sekolah',
                })

    created_count = 0
    for data in attendance_data:
        _, created = Attendance.objects.get_or_create(
            student=data['student'],
            sekolah=data['sekolah'],
            date=data['date'],
            absen_type=data['absen_type'],
            defaults=data
        )
        if created:
            created_count += 1
    
    print(f"Attendance records seeded successfully! ({created_count} new records created)")


def seed_attendance_permissions():
    students = Student.objects.filter(status_aktif=True)
    
    permission_data = []
    today = timezone.now().date()
    
    # Sample reasons for permissions
    sakit_reasons = [
        "Demam dan flu",
        "Sakit perut",
        "Terapi medis",
        "Check up dokter",
        "Rawat inap"
    ]
    
    izin_reasons = [
        "Acara keluarga",
        "Kompetisi akademik", 
        "Kegiatan OSIS",
        "Urusan keluarga penting",
        "Acara keagamaan"
    ]
    
    # Sample accept statuses with weighted probabilities
    accept_statuses = ['PENDING', 'APPROVED', 'REJECTED']
    accept_weights = [0.3, 0.5, 0.2]  # 30% pending, 50% approved, 20% rejected
    
    for student in students:
        school = student.sekolah
        if school:
            # Create permissions for the last 30 days
            for i in range(30):
                # Only create permission with 20% probability
                if random.random() < 0.2:
                    date = today - timedelta(days=i)
                    
                    # Randomly choose between SAKIT and IZIN
                    permission_type = random.choice(['SAKIT', 'IZIN'])
                    reason = random.choice(sakit_reasons if permission_type == 'SAKIT' else izin_reasons)
                    
                    # Random accept status based on weights
                    accept_status = random.choices(accept_statuses, weights=accept_weights, k=1)[0]
                    
                    permission_data.append({
                        'id': uuid.uuid4(),
                        'student': student,
                        'sekolah': school,
                        'date': date,
                        'permission_type': permission_type,
                        'reason': reason,
                        'accept_status': accept_status,
                        # Document field is left empty since it's a file field
                        'document': None
                    })

    created_count = 0
    for data in permission_data:
        try:
            # Try to create permission if it doesn't exist
            _, created = AttendancePermission.objects.get_or_create(
                student=data['student'],
                sekolah=data['sekolah'],
                date=data['date'],
                permission_type=data['permission_type'],
                defaults={
                    'id': data['id'],
                    'reason': data['reason'],
                    'accept_status': data['accept_status'],
                    'document': data['document']
                }
            )
            if created:
                created_count += 1
        except Exception as e:
            print(f"Error creating permission: {str(e)}")
            continue
    
    print(f"Attendance permissions seeded successfully! ({created_count} new permissions created)")
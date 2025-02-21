from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.utils.text import slugify

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('GURU', 'Guru'), 
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES)
    nama_lengkap = models.CharField(max_length=100)
    status_aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
        
    def has_module_perms(self, app_label):
        return self.is_superuser
    
class Student(models.Model):
    STATUS_CHOICES = [
        ('AKTIF', 'Aktif'),
        ('ALUMNI', 'Alumni'),
        ('PINDAH', 'Pindah'),
        ('DIKELUARKAN', 'Dikeluarkan')
    ]

    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan')
    ]

    BLOOD_TYPE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, editable=False)  # New field
    nisn = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    nama_lengkap = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nomor_whatsapp = models.CharField(max_length=15)
    tinggi_badan = models.IntegerField(help_text='Tinggi badan dalam cm')
    berat_badan = models.IntegerField(help_text='Berat badan dalam kg')
    golongan_darah = models.CharField(max_length=2, choices=BLOOD_TYPE_CHOICES)
    status_siswa = models.CharField(max_length=11, choices=STATUS_CHOICES)
    status_aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sekolah = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name='Sekolah',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.username:
            
            base_username = slugify(self.nama_lengkap.lower().replace(" ", ""))
            username = base_username
            counter = 1
            
            while Student.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
                
            self.username = username
            
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'siswa'
        verbose_name = 'Siswa'
        verbose_name_plural = 'Siswa'

class School(models.Model):
    STATUS_CHOICES = [
        ('AKTIF', 'Aktif'),
        ('TIDAK_AKTIF', 'Tidak Aktif')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    npsn = models.CharField(max_length=8, unique=True)
    nama_sekolah = models.CharField(max_length=100)
    alamat = models.TextField()
    kota = models.CharField(max_length=50)
    provinsi = models.CharField(max_length=50)
    kode_pos = models.CharField(max_length=5)
    telepon = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    kepala_sekolah = models.CharField(max_length=100)
    guru = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'GURU'},
        related_name='sekolah'
    )
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='AKTIF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sekolah'
        verbose_name = 'Sekolah'
        verbose_name_plural = 'Sekolah'

    def __str__(self):
        return f"{self.npsn} - {self.nama_sekolah}"
    
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('HADIR', 'Hadir'),
        ('ALPA', 'Alpa'),
    ]

    ABSEN_TYPE_CHOICES = [
        ('MASUK', 'Masuk'),
        ('PULANG', 'Pulang')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)  # Add time field
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    absen_type = models.CharField(max_length=6, choices=ABSEN_TYPE_CHOICES)
    location = models.CharField(max_length=255, null=True, blank=True)  # Add location field
    photo = models.ImageField(upload_to='attendance_photos/', null=True, blank=True)  # Add photo field
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    sekolah = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        unique_together = ['date', 'student', 'sekolah', 'absen_type']

    def __str__(self):
        return f"{self.student.nama_lengkap} - {self.date} - {self.time} - {self.status} - {self.get_absen_type_display()}"


class AttendancePermission(models.Model):
    PERMISSION_TYPE_CHOICES = [
        ('SAKIT', 'Sakit'),
        ('IZIN', 'Izin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    sekolah = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    date = models.DateField()
    permission_type = models.CharField(max_length=5, choices=PERMISSION_TYPE_CHOICES)
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        unique_together = ['date', 'student', 'sekolah', 'permission_type']

    def __str__(self):
        return f"{self.student.nama_lengkap} - {self.date} - {self.get_permission_type_display()}"

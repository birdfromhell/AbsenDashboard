from rest_framework import serializers
from Dashboard.models import School, User, Student, Attendance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nama_lengkap', 'email']

class SchoolSerializer(serializers.ModelSerializer):
    guru = UserSerializer(read_only=True)
    
    class Meta:
        model = School
        fields = [
            'id', 'npsn', 'nama_sekolah', 'alamat', 'kota', 
            'provinsi', 'kode_pos', 'telepon', 'email', 
            'website', 'kepala_sekolah', 'guru', 'status'
        ]

class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='sekolah.nama_sekolah', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'nama_lengkap', 'sekolah', 'school_name', 'status_aktif']

class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    school_id = serializers.UUIDField()


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.nama_lengkap', read_only=True)
    school_name = serializers.CharField(source='sekolah.nama_sekolah', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    absen_type_display = serializers.CharField(source='get_absen_type_display', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'date', 'time', 'status', 'status_display',
            'absen_type', 'absen_type_display', 'location', 'photo',
            'student', 'student_name', 'sekolah', 'school_name',
            'created_at', 'updated_at'
        ]


class AttendanceImageHistorySerializer(serializers.ModelSerializer):
    absen_type_display = serializers.CharField(source='get_absen_type_display', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['absen_type', 'absen_type_display', 'photo', 'location', 'time', 'date']
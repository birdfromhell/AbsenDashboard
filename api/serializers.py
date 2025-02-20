from rest_framework import serializers
from Dashboard.models import School, User, Student

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
            'website', 'kepala_sekolah', 'guru', 'status',
            'created_at', 'updated_at'
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


from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.hashers import check_password
from Dashboard.models import Student, School, Attendance
from .serializers import StudentSerializer, StudentLoginSerializer, SchoolSerializer, AttendanceSerializer
from django.utils import timezone


@api_view(['GET'])
@permission_classes([AllowAny])
def check_session(request):
    return Response({
        'status': 200,
        'message': 'Session is valid',
        'data': None
    })

class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        try:
            schools = self.get_queryset()
            serializer = self.get_serializer(schools, many=True)
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'Data sekolah berhasil diambil'
            })
        except Exception as e:
            return Response({
                'status': 500,
                'message': str(e),
                'type': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def student_login(request):
    serializer = StudentLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'status': 400,
            'message': 'Username, password, dan sekolah harus diisi',
            'type': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    school_id = serializer.validated_data['school_id']

    try:
        student = Student.objects.get(username=username, sekolah_id=school_id)
        
        if not check_password(password, student.password):
            return Response({
                'status': 401,
                'message': 'Password salah',
                'type': 'error'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(student)
        
        return Response({
            'status': 200,
            'data': {
                'token': str(refresh.access_token),
                'user': {
                    'username': student.username,
                    'school_name': student.sekolah.nama_sekolah if student.sekolah else None
                }
            },
            'message': 'Login berhasil'
        })

    except Student.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'User tidak ditemukan di sekolah tersebut',
            'type': 'error'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'status': 500,
            'message': 'Terjadi kesalahan di server',
            'type': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self, request):
        try:
            students = self.get_queryset()
            serializer = self.get_serializer(students, many=True)
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'ambil semua data user'
            })
        except Exception as e:
            return Response({
                'status': 500,
                'message': 'gagal',
                'type': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Attendance.objects.all()
        student_id = self.request.query_params.get('student', None)
        school_id = self.request.query_params.get('school', None)
        date = self.request.query_params.get('date', None)
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if school_id:
            queryset = queryset.filter(sekolah_id=school_id)
        if date:
            queryset = queryset.filter(date=date)
            
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            request.data['date'] = request.data.get('date', timezone.now().date())
            serializer = self.get_serializer(data=request.data)
            
            if not serializer.is_valid():
                return Response({
                    'status': 400,
                    'message': 'Data tidak valid',
                    'errors': serializer.errors,
                    'type': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)

            self.perform_create(serializer)
            return Response({
                'status': 201,
                'data': serializer.data,
                'message': 'Absensi berhasil dicatat'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'status': 500,
                'message': str(e),
                'type': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'Data absensi berhasil diambil'
            })
        except Exception as e:
            return Response({
                'status': 500,
                'message': str(e),
                'type': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance_image_history(request, user_id):
    try:
        attendances = Attendance.objects.filter(
            student_id=user_id,
            photo__isnull=False
        ).order_by('-date', '-time').values(
            'absen_type',
            'photo',
            'location',
            'time',
            'date'
        )

        return Response({
            'status': 200,
            'data': attendances,
            'message': 'Data riwayat foto absensi berhasil diambil'
        })
    except Exception as e:
        return Response({
            'status': 500,
            'message': str(e),
            'type': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from Dashboard.models import Student, School, Attendance,AttendancePermission
from .serializers import StudentSerializer,AttendancePermissionSerializer, StudentLoginSerializer, SchoolSerializer, AttendanceSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_description="Check if user session is valid",
    responses={200: 'Session is valid'}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def check_session(request):
    return Response({
        'status': 200,
        'message': 'Session is valid',
        'data': None
    })

class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing school data.
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Get list of all schools",
        responses={200: SchoolSerializer(many=True)}
    )
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

@swagger_auto_schema(
    method='post',
    operation_description="Login for students",
    request_body=StudentLoginSerializer,
    responses={
        200: openapi.Response('Login successful'),
        400: 'Invalid input',
        401: 'Invalid credentials',
        404: 'Student not found',
        500: 'Server error'
    }
)


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
    """
    ViewSet for managing student data.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @swagger_auto_schema(
        operation_description="Get list of all students",
        responses={200: StudentSerializer(many=True)}
    )
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
    """
    ViewSet for managing attendance records.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get filtered attendance records",
        manual_parameters=[
            openapi.Parameter('student', openapi.IN_QUERY, description="Filter by student ID", type=openapi.TYPE_STRING),
            openapi.Parameter('school', openapi.IN_QUERY, description="Filter by school ID", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_QUERY, description="Filter by date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={200: AttendanceSerializer(many=True)}
    )
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

    @swagger_auto_schema(
        operation_description="Create new attendance record",
        request_body=AttendanceSerializer,
        responses={
            201: AttendanceSerializer,
            400: 'Invalid data',
            500: 'Server error'
        }
    )
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

@swagger_auto_schema(
    method='get',
    operation_description="Get attendance image history for a user",
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_STRING, required=True),
    ],
    responses={
        200: openapi.Response('Success'),
        500: 'Server error'
    }
)
@api_view(['GET'])
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
    
class AttendancePermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing attendance permission records.
    """
    queryset = AttendancePermission.objects.all()
    serializer_class = AttendancePermissionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get filtered attendance permission records",
        manual_parameters=[
            openapi.Parameter('student', openapi.IN_QUERY, description="Filter by student ID", type=openapi.TYPE_STRING),
            openapi.Parameter('school', openapi.IN_QUERY, description="Filter by school ID", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_QUERY, description="Filter by date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status (PENDING/APPROVED/REJECTED)", type=openapi.TYPE_STRING),
        ],
        responses={200: AttendancePermissionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            
            # Apply filters
            student_id = request.query_params.get('student')
            school_id = request.query_params.get('school')
            date = request.query_params.get('date')
            status = request.query_params.get('status')

            if student_id:
                queryset = queryset.filter(student_id=student_id)
            if school_id:
                queryset = queryset.filter(sekolah_id=school_id)
            if date:
                queryset = queryset.filter(date=date)
            if status:
                queryset = queryset.filter(accept_status=status)

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'Data izin berhasil diambil'
            })
        except Exception as e:
            return Response({
                'status': 500,
                'message': str(e),
                'type': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Create new attendance permission request",
        request_body=AttendancePermissionSerializer,
        responses={
            201: AttendancePermissionSerializer,
            400: 'Invalid data',
            500: 'Server error'
        }
    )
    def create(self, request, *args, **kwargs):
        try:
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
                'message': 'Permintaan izin berhasil dibuat'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 500,
                'message': str(e),
                'type': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from Dashboard.models import Student, School
from .serializers import StudentSerializer, StudentLoginSerializer, SchoolSerializer


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
        
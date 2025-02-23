from .models import AttendancePermission, School

def pending_permissions(request):
    if request.user.is_authenticated and request.user.role == 'GURU':
        school = School.objects.filter(guru=request.user).first()
        if school:
            pending_count = AttendancePermission.objects.filter(
                sekolah=school,
                accept_status='PENDING'
            ).count()
            return {'pending_permissions_count': pending_count}
    return {'pending_permissions_count': 0}
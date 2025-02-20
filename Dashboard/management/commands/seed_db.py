from django.core.management.base import BaseCommand
from Dashboard.seeders import seed_users, seed_students, seed_schools, seed_attendance
from Dashboard.models import User, Student, School, Attendance

class Command(BaseCommand):
    help = 'seed database'

    def handle(self, *args, **kwargs):

        if User.objects.count() == 0:
            self.stdout.write('Seeding users...')
            seed_users()
        else:
            self.stdout.write('Users already exist, skipping...')
 
        if Student.objects.count() == 0:
            self.stdout.write('Seeding students...')
            seed_students()
        else:
            self.stdout.write('Students already exist, skipping...')

        if School.objects.count() == 0:
            self.stdout.write('Seeding schools...')
            seed_schools()
        else:
            self.stdout.write('Schools already exist, skipping...')

        if Attendance.objects.count() == 0:
            self.stdout.write('Seeding attendance records...')
            seed_attendance()
        else:
            self.stdout.write('Attendance records already exist, skipping...')

        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
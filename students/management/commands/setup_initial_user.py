from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student
from django.utils.timezone import localdate
from datetime import timedelta

class Command(BaseCommand):
    help = 'Setup initial student user for Render deployment'

    def handle(self, *args, **kwargs):
        from django.conf import settings
        db_engine = settings.DATABASES['default']['ENGINE']
        self.stdout.write(f"Using database engine: {db_engine}")
        
        username = 'nimstudent'
        password = '123'
        email = 'nimstudent@example.com'

        # 1. Create User
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.email = email
            user.first_name = "Nim"
            user.last_name = "Student"
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists. Updating password.'))
            user.set_password(password)
            user.save()

        # 2. Create Student Profile (required by student_login_api)
        student, s_created = Student.objects.get_or_create(user=user)
        if s_created:
            student.phone = "1234567890"
            student.password_plain = password
            student.valid_upto = localdate() + timedelta(days=300) # 10 months
            student.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created student profile for: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Student profile for {username} already exists.'))

        # 3. Create Superuser (optional but helpful)
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser: admin / admin123'))

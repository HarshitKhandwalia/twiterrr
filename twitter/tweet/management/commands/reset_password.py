from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Reset superuser password'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to reset password for')
        parser.add_argument('new_password', type=str, help='New password')

    def handle(self, *args, **options):
        username = options['username']
        new_password = options['new_password']
        
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully reset password for user "{username}"')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            ) 
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def handle(self, *args, **options):
        user_model = get_user_model()
        admin = user_model.objects.filter(email='test@test.com')

        if not admin.exists():
            user_model.objects.create_superuser(email='test@test.com',
                                                username='test@test.com',
                                                password='1234567',
                                                first_name='Admin',
                                                last_name='Adminovich')

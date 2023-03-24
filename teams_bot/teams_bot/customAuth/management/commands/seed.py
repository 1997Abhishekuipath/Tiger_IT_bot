from django.db import transaction
from django.core.management.base import BaseCommand
from customAuth.models.model_user import User


class Command(BaseCommand):
    help = 'base seeder'

    def handle(self, *args, **options):
        with transaction.atomic():
            # admin user
            user = User(
                email='admin@demo.com',
                is_superuser=True,
                is_staff=True,
                is_active=True
            )
            user.set_password('12345')
            user.save()

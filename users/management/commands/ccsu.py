from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='karpukhinvitaliy0128@gmail.com',
            first_name='Vitaliy',
            last_name='Karpukhin',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('123456789')
        user.save()

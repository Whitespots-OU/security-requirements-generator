from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as BaseUser
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.utils.crypto import get_random_string

User: BaseUser = get_user_model()


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("-u", "--username", default="admin", type=str, help="New user username")
        parser.add_argument("-e", "--email", default="admin@example.com", type=str, help="New user email")
        parser.add_argument("-p", "--password", default="admin", type=str, help="New user password")
        parser.add_argument("-r", "--random-password", action="store_true", help="Use random password")

    def handle(self, *args, **options):
        try:
            user = User.objects.create(
                username=options["username"], email=options["email"], is_superuser=True, is_staff=True
            )

            if options["random_password"]:
                password = get_random_string(length=16)
                self.stdout.write(f'Random password is "{password}"', self.style.SUCCESS)
            else:
                password = options["password"]

            user.set_password(password)
            user.save()
        except IntegrityError:
            self.stdout.write(f'Username "{options["username"]}" is already exists', self.style.WARNING)
        except Exception as e:
            raise CommandError(str(e))

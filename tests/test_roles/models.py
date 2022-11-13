from django.contrib.auth.models import AbstractUser

from django_ram.roles.models import RolesMixin


class CustomUser(AbstractUser, RolesMixin):
    class Meta:
        abstract = False

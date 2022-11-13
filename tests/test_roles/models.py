from django.contrib.auth.models import AbstractUser

from rest_iam.roles.models import RolesMixin


class CustomUser(AbstractUser, RolesMixin):
    class Meta:
        abstract = False

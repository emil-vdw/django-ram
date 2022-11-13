from django.contrib import admin

from django_ram.admin import UserAdmin
from tests.test_roles.models import CustomUser

admin.site.register(CustomUser, UserAdmin)

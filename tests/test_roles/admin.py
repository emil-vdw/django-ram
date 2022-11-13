from django.contrib import admin
from rest_iam.roles.admin import UserAdmin
from tests.test_roles.models import CustomUser

admin.site.register(CustomUser, UserAdmin)

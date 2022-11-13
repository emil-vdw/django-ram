import django

if django.VERSION < (3, 2):
    default_app_config = "rest_iam.roles.apps.RolesConfig"

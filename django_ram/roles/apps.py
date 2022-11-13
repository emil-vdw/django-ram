from django.apps import AppConfig
from django.db.models.signals import post_migrate


class RolesConfig(AppConfig):
    name = "django_ram.roles"
    verbose_name = "Roles"

    def ready(self) -> None:
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules("roles")
        from django_ram.roles.definition import create_roles

        post_migrate.connect(create_roles, sender=self)
        return super().ready()

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_roles(sender, **kwargs):
    """Create role DB records from role definitions."""
    from rest_iam.roles.definition import role_definitions
    from rest_iam.roles.models import Role

    for role_definition in role_definitions:
        Role.objects.get_or_create(name=role_definition.name)


class RolesConfig(AppConfig):
    name = "rest_iam.roles"
    verbose_name = "Roles"

    def ready(self) -> None:
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules("roles")
        post_migrate.connect(create_roles, sender=self)
        return super().ready()

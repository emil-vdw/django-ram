from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_roles(sender, **kwargs):
    """Create role DB records from role definitions."""
    from django_ram.roles.definition import (
        ROLE_DEFINITION_ATTRIBUTES, role_definitions
    )
    from django_ram.roles.models import Role

    for role_definition in role_definitions:
        role, _ = Role.objects.get_or_create(
            name=role_definition.name,
        )
        role_attributes = [
            attribute_name
            for attribute_name in ROLE_DEFINITION_ATTRIBUTES
            if attribute_name != "name" and hasattr(role_definition, attribute_name)
        ]
        for attribute_name in role_attributes:
            setattr(role, attribute_name, getattr(role_definition, attribute_name))
            role.save(update_fields=role_attributes)


class RolesConfig(AppConfig):
    name = "django_ram.roles"
    verbose_name = "Roles"

    def ready(self) -> None:
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules("roles")
        post_migrate.connect(create_roles, sender=self)
        return super().ready()

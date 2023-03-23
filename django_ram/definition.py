"""Classes and utilities used to define user roles."""


role_definitions = set()


REQUIRED_ROLE_DEFNITION_ATTRIBUTES = {"name"}
ROLE_DEFINITION_ATTRIBUTES = {*REQUIRED_ROLE_DEFNITION_ATTRIBUTES, "description"}


def create_roles(sender, plan=None, **kwargs):
    """Create :class:`~django_ram.models.Role`\s from :class:`~django_ram.definition.RoleDefinition`\s."""
    unapplying = plan and any([unapply for _, unapply in plan])
    if unapplying:
        return

    from django_ram.definition import ROLE_DEFINITION_ATTRIBUTES, role_definitions
    from django_ram.models import Role

    for role_definition in role_definitions:
        role, _ = Role.objects.get_or_create(name=role_definition.name)
        role_attributes = [
            attribute_name
            for attribute_name in ROLE_DEFINITION_ATTRIBUTES
            if attribute_name != "name" and hasattr(role_definition, attribute_name)
        ]
        for attribute_name in role_attributes:
            setattr(role, attribute_name, getattr(role_definition, attribute_name))
            role.save(update_fields=role_attributes)


def clean_removed_roles(sender, plan=None, **kwargs):
    """Delete or mark as inactive all roles that do not have a definition (role definition has been removed).

    If the ``DELETE_REMOVED_ROLES`` setting is enabled, delete all roles without a corresponding
    :class:`~django_ram.definition.RoleDefinition`. Otherwise, only set ``active`` to `False`.
    """
    unapplying = plan and any([unapply for _, unapply in plan])
    if unapplying:
        return

    from django.conf import settings

    from django_ram.definition import role_definitions
    from django_ram.models import Role

    removed_roles = Role.objects.exclude(
        name__in={role_definition.name for role_definition in role_definitions}
    )

    if getattr(settings, "DELETE_REMOVED_ROLES", False):
        removed_roles.delete()
    else:
        removed_roles.update(active=False)


def _verify_role_definition_attributes(role_definition_class_name, role_attributes):
    for attribute_name in REQUIRED_ROLE_DEFNITION_ATTRIBUTES:
        assert role_attributes.get(
            attribute_name
        ), f"Role definition '{role_definition_class_name}' is missing required attribute '{attribute_name}'"

        assert role_attributes["name"] not in [
            role_definition.name for role_definition in role_definitions
        ], (
            f"Role definition '{role_definition_class_name}' "
            f"has role name '{role_attributes['name']}' that already exists"
        )


class RoleDefinitionBase(type):
    """Metaclass for all role definitions."""

    def __new__(cls, name, bases, attrs, **kwargs):
        """Register role definition classes to create role records post-migration."""
        if name == "RoleDefinition":
            return super().__new__(cls, name, bases, attrs, **kwargs)

        _verify_role_definition_attributes(name, attrs)
        new_role_definition = super().__new__(cls, name, bases, attrs, **kwargs)
        role_definitions.add(new_role_definition)

        return new_role_definition


class RoleDefinition(metaclass=RoleDefinitionBase):
    """
    A class used to define a :class:`~django_ram.models.Role`.
    """

    #: Role name
    name: str
    #: Role description
    description: str = ""

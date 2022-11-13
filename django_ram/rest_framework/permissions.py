"""Rest framework role based permission classes."""
from typing import Optional, Type

from rest_framework.permissions import BasePermission

from django_ram.roles.definition import RoleDefinition


class HasRoleBasePermission(BasePermission):
    role_definition: Type[RoleDefinition]

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.has_role(self.role_definition.name)
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


def generate_permission_name_from_role_definition(role: Type[RoleDefinition]):
    role_name_camelcase = role.name.title().replace("_", "").replace(" ", "")
    permission_class_name = f"Has{role_name_camelcase}"

    if not permission_class_name.endswith("Role"):
        permission_class_name += "Role"

    return permission_class_name


def has_role(role_definition: Type[RoleDefinition], class_name: Optional[str] = None):
    return type(
        class_name or generate_permission_name_from_role_definition(role_definition),
        (HasRoleBasePermission,),
        dict(
            role_definition=role_definition,
        ),
    )

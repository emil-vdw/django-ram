"""Classes and utilities used to define user roles."""
role_definitions = set()


class RoleDefinitionBase(type):
    """Metaclass for all role definitions."""

    def __new__(cls, name, bases, attrs, **kwargs):
        """Register role definition classes to create role records post-migration."""
        new_role_definition = super().__new__(cls, name, bases, attrs, **kwargs)
        if name != "RoleDefinition":
            role_definitions.add(new_role_definition)
        return new_role_definition


class RoleDefinition(metaclass=RoleDefinitionBase):
    name: str

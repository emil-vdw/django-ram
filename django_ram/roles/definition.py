"""Classes and utilities used to define user roles."""
role_definitions = set()


REQUIRED_ROLE_DEFNITION_ATTRIBUTES = {
    "name",
}
ROLE_DEFINITION_ATTRIBUTES = {
    *REQUIRED_ROLE_DEFNITION_ATTRIBUTES,
    "description",
}


def _verify_role_definition_attributes(role_definition_class_name, role_attributes):
    for attribute_name in REQUIRED_ROLE_DEFNITION_ATTRIBUTES:
        assert role_attributes.get(
            attribute_name
        ), f"Role definition '{role_definition_class_name}' is missing required attribute '{attribute_name}'"
        assert role_attributes["name"] not in [
            role_definition.name for role_definition in role_definitions
        ], f"Role '{role_definition_class_name}' has name '{role_attributes['name']}' that already exists"


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
    name: str

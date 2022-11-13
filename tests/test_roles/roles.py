from django_ram.roles.definition import RoleDefinition


class Administrator(RoleDefinition):
    name = "Admin"


class Author(RoleDefinition):
    name = "Author"

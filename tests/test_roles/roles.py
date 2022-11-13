from django_ram.definition import RoleDefinition


class Administrator(RoleDefinition):
    name = "Admin"


class Author(RoleDefinition):
    name = "Author"

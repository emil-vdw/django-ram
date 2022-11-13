from rest_iam.roles.definition import RoleDefinition


class Administrator(RoleDefinition):
    name = "Admin"


class Author(RoleDefinition):
    name = "Author"

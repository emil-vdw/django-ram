from django_ram.definition import RoleDefinition


class Administrator(RoleDefinition):
    name = "Admin"
    description = "System administrator."


class Author(RoleDefinition):
    name = "Author"
    description = "A writer of a book, article, or document."

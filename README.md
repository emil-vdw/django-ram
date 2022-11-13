# [Django RAM]

Role based user access management for Django.

# Requirements

* Python 3.6+
* Django 4.1, 4.0, 3.2, 3.1, 3.0

# Overview

## Declarative Roles

```python
# some_app/roles.py
from django_ram.roles import RoleDefinition


class AdminRole(RoleDefinition):
    name = "Admin"
    description = "System administrator."


class AuthorRole(RoleDefinition):
    name = "Author"
    description = "A writer of a book, article, or document."
```

Roles will be created post migrations to reflect role definitions in `roles.py` files.

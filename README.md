# Django RAM

Role based user access management for Django.

# Requirements

* Python 3.6+
* Django 4.1, 4.0, 3.2, 3.1, 3.0

# Installation

    pip install django-ram
    
Optionally install with rest framework support:

    pip install django-ram[rest_framework]

    
Add `django_ram'` to your `INSTALLED_APPS` setting.
```python
INSTALLED_APPS = [
    ...
    'django_ram',
]
```

    ./manage.py migrate

# Overview

## User Model

Add the `RolesMixin` to your user model.

```python
from django_ram.models import RolesMixin


class CustomUser(AbstractUser, RolesMixin):
    pass
```

Also remember to configure `AUTH_USER_MODEL` in your `settings.py` module.


## Declarative Roles
some_app/roles.py

```python
from django_ram.definition import RoleDefinition


class AdminRole(RoleDefinition):
    name = "Admin"
    description = "System administrator."


class AuthorRole(RoleDefinition):
    name = "Author"
    description = "A writer of a book, article, or document."
```

Roles will be created (or updated) post migration to reflect role definitions in `roles.py` files.

Role names have to be globally unique.


## Django Admin

Register the admin class (or subclass it to expand functionality.)

```python
from django.contrib import admin
from django_ram.admin import UserAdmin

...

admin.site.register(YourUserModel, UserAdmin)
```


## Rest Framework Support

```python
from django_ram.rest_framework import HasRoleBasePermission, has_role
from some_app.roles import AuthorRole


class HasAuthorRole(HasRoleBasePermission):
    role_definition = AuthorRole


class PublicationViewSet(viewsets.ModelViewset):
    permission_classes = [
        has_role(AuthorRole),
        #  Is equivelant to:
        HasAuthorRole,
    ]
```

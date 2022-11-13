Overview
========

Roles
-----

The :class:`django_ram.models.Role` model stores user roles through a
many to many relationship from the user model.


User Model
----------

In order to use roles, it is required to use the
:class:`~django_ram.models.RolesMixin` with your user model.

.. code-block:: python

    from django_ram.models import RolesMixin


    class CustomUser(AbstractUser, RolesMixin):
        pass


Defining Roles
--------------

Roles are defined in code, rather than being created manually. Roles
have to be defined in a ``roles`` module inside of django apps.
For example:

::

    project
    └── some_app
        ├── models.py
        ├── ...
        └── roles.py


.. code-block:: python
   :caption: roles.py

    from django_ram.definition import RoleDefinition


    class AdminRole(RoleDefinition):
        name = "Admin"
        description = "System administrator."    
                

    class AuthorRole(RoleDefinition):
        name = "Author"
        description = "A writer of a book, article, or document."


.. important:: Role names have to be unique across all apps.

Roles database records will automatically be created after applying
migrations. If changes are made to role definitions, by changing the
description for example, those roles will be updated when applying
migrations.

.. note:: When role definitions are removed or renamed, old role
          records have to be deleted manually.


Django Admin
------------

Register the admin class (or subclass it to expand functionality.)

.. code-block:: python

    from django.contrib import admin
    from django_ram.admin import UserAdmin

    
    admin.site.register(YourUserModel, UserAdmin)


This will add the roles field to the user admin using the same widget
as the Django `user_permissions` and `groups` fields.


Rest Framework integration
--------------------------

Use the :func:`~django_ram.rest_framework.permissions.has_role` DRF permission class factory function to
restrict access to views based on user roles. You can also subclass
:class:`~django_ram.rest_framework.permissions.HasRoleBasePermission` to extend the permission check logic.

.. code-block:: python

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

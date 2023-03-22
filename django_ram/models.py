from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)
    description = models.TextField(verbose_name=_("Description"))
    active = models.BooleanField(verbose_name=_("Active"), blank=True, default=True)

    class Meta(object):
        abstract = "django_ram" not in settings.INSTALLED_APPS

    def __str__(self) -> str:
        return self.name


class RolesMixin(models.Model):
    """Adds fields and methods to support User Roles."""

    roles = models.ManyToManyField(
        Role,
        verbose_name=_("roles"),
        blank=True,
        help_text=_("Specific roles for this user."),
        related_name="users",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    @classmethod
    def with_role(cls, role: Union[Role, str], is_active=True, include_superusers=True):
        """
        Return queryset of users with ``role``.

        :param role: Return users with this role.
        :param is_active: Include active (`True`), inactive (`False`), or all users (`None`).
        :param include_superusers: Whether to include superusers in the result.

        :return: Queryset of users with ``role``.
        """
        UserModel = get_user_model()
        role_query = models.Q(user=models.OuterRef("pk"))

        if isinstance(role, Role):
            role_query &= models.Q(pk=role.pk)
        elif isinstance(role, str):
            role_query &= models.Q(name=role)
        else:
            raise TypeError("The `role` argument must be a string or a Role instance.")

        user_query = models.Exists(Role.objects.filter(role_query))

        if include_superusers:
            user_query |= models.Q(is_superuser=True)
        if is_active is not None:
            user_query &= models.Q(is_active=is_active)

        return UserModel._default_manager.filter(user_query)

    def has_role(self, role_name: str):
        """
        Return `True` if the user is a superuser or has the role with name ``role_name``.

        :param role_name: Name of the role to check.
        """
        return self.is_active and (
            self.is_superuser or self.roles.filter(name=role_name).exists()
        )

    def get_roles(self):
        """Return a list of role names associated with this user."""
        return set(self.roles.values_list("name", flat=True))

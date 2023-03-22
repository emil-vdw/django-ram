from django.apps import AppConfig
from django.db.models.signals import post_migrate


class DjangoRamConfig(AppConfig):
    name = "django_ram"
    verbose_name = "Django RAM"

    def ready(self) -> None:
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules("roles")
        from django_ram.definition import clean_removed_roles, create_roles

        post_migrate.connect(create_roles, sender=self)
        post_migrate.connect(clean_removed_roles, sender=self)
        return super().ready()

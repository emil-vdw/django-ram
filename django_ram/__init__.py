"""Django RAM."""

import django

__version__ = "0.1"
VERSION = __version__

if django.VERSION < (3, 2):
    default_app_config = "django_ram.apps.DjangoRamConfig"

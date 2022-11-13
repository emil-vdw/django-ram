Installation
============

.. code-block::

    pip install django-ram


Optionally install with rest framework support:

.. code-block::

    pip install django-ram[rest_framework]

    
Add ``django_ram`` to `INSTALLED_APPS` in your ``settings.py`` file.

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'django_ram',
    ]

.. code-block::

    ./manage.py migrate

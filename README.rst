DJ-Database-URL
~~~~~~~~~~~~~~

This simple Django utility allows you to utilize the
`12factor <http://www.12factor.net/backing-services>`_ inspired
``DATABASE_URL`` environment variable to configure your Django application.


Usage
-----

Configure your database in ``settings.py`` from ``DATABASE_URL``::

    DATABASES['default'] = dj_database_url.config()

Parse an arbitrary Database URL::

    DATABASES['default'] = dj_database_url.parse('postgres://...')


Installation
------------

Installation is simple too::

    $ pip install dj-database-url
DJ-Database-URL
~~~~~~~~~~~~~~

This simple Django utility allows you to utilize the
`12factor <http://www.12factor.net/backing-services>`_ inspired
``DATABASE_URL`` environment variable to configure your Django application.


Usage
-----

Configure your database in ``settings.py`` from ``DATABASE_URL``::

    DATABASES = {'default': dj_database_url.config()}

Parse an arbitrary Database URL::

    DATABASES = {'default': dj_database_url.parse('postgres://...')}

Supported databases
-------------------

Support currently exists for PostgreSQL, MySQL and SQLite.

SQLite connects to file based databases. The same URL format is used, omitting
the hostname, and using the "file" portion as the filename of the database.
This has the effect of four slashes being present for an absolute file path:
``sqlite:////full/path/to/your/database/file.sqlite``.

Installation
------------

Installation is simple too::

    $ pip install dj-database-url

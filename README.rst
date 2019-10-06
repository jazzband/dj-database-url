DJ-Database-URL
~~~~~~~~~~~~~~~

.. image:: https://secure.travis-ci.org/jacobian/dj-database-url.svg?branch=master
   :target: http://travis-ci.org/jacobian/dj-database-url

This simple Django utility allows you to utilize the
`12factor <http://www.12factor.net/backing-services>`_ inspired
``DATABASE_URL`` environment variable to configure your Django application.

The ``dj_database_url.config`` method returns a Django database connection
dictionary, populated with all the data specified in your URL. There is
also a `conn_max_age` argument to easily enable Django's connection pool.

If you'd rather not use an environment variable, you can pass a URL in directly
instead to ``dj_database_url.parse``.

Supported Databases
-------------------

Support currently exists for PostgreSQL, PostGIS, MySQL, MySQL (GIS),
Oracle, Oracle (GIS), Redshift, and SQLite.

Installation
------------

Installation is simple::

    $ pip install dj-database-url

Usage
-----

Configure your database in ``settings.py`` from ``DATABASE_URL``::

    import dj_database_url

    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

Provide a default::

    DATABASES['default'] = dj_database_url.config(default='postgres://...')

Parse an arbitrary Database URL::

    DATABASES['default'] = dj_database_url.parse('postgres://...', conn_max_age=600)

The ``conn_max_age`` attribute is the lifetime of a database connection in seconds
and is available in Django 1.6+. If you do not set a value, it will default to ``0``
which is Django's historical behavior of using a new database connection on each
request. Use ``None`` for unlimited persistent connections.

Strings passed to ``dj_database_url`` must actually be valid URLs; in
particular, special characters must be url-encoded. The following url will raise
a ``ValueError``

    postgres://user:p#ssword!@localhost/foobar

and should instead be passed as

    postgres://user:p%23ssword!@localhost/foobar

URL schema
----------

+-------------+-----------------------------------------------+--------------------------------------------------+
| Engine      | Django Backend                                | URL                                              |
+=============+===============================================+==================================================+
| PostgreSQL  | ``django.db.backends.postgresql`` [1]_        | ``postgres://USER:PASSWORD@HOST:PORT/NAME`` [2]_ |
+-------------+-----------------------------------------------+--------------------------------------------------+
| PostGIS     | ``django.contrib.gis.db.backends.postgis``    | ``postgis://USER:PASSWORD@HOST:PORT/NAME``       |
+-------------+-----------------------------------------------+--------------------------------------------------+
| MSSQL       | ``sql_server.pyodbc``                         | ``mssql://USER:PASSWORD@HOST:PORT/NAME``         |
+-------------+-----------------------------------------------+--------------------------------------------------+
| MySQL       | ``django.db.backends.mysql``                  | ``mysql://USER:PASSWORD@HOST:PORT/NAME``         |
+-------------+-----------------------------------------------+--------------------------------------------------+
| MySQL (GIS) | ``django.contrib.gis.db.backends.mysql``      | ``mysqlgis://USER:PASSWORD@HOST:PORT/NAME``      |
+-------------+-----------------------------------------------+--------------------------------------------------+
| SQLite      | ``django.db.backends.sqlite3``                | ``sqlite:///PATH`` [3]_                          |
+-------------+-----------------------------------------------+--------------------------------------------------+
| SpatiaLite  | ``django.contrib.gis.db.backends.spatialite`` | ``spatialite:///PATH`` [3]_                      |
+-------------+-----------------------------------------------+--------------------------------------------------+
| Oracle      | ``django.db.backends.oracle``                 | ``oracle://USER:PASSWORD@HOST:PORT/NAME`` [4]_   |
+-------------+-----------------------------------------------+--------------------------------------------------+
| Oracle (GIS)| ``django.contrib.gis.db.backends.oracle``     | ``oraclegis://USER:PASSWORD@HOST:PORT/NAME``     |
+-------------+-----------------------------------------------+--------------------------------------------------+
| Redshift    | ``django_redshift_backend``                   | ``redshift://USER:PASSWORD@HOST:PORT/NAME``      |
+-------------+-----------------------------------------------+--------------------------------------------------+

.. [1] The django.db.backends.postgresql backend is named django.db.backends.postgresql_psycopg2 in older releases. For
       backwards compatibility, the old name still works in newer versions. (The new name does not work in older versions).
.. [2] With PostgreSQL, you can also use unix domain socket paths with
       `percent encoding <http://www.postgresql.org/docs/9.2/interactive/libpq-connect.html#AEN38162>`_:
       ``postgres://%2Fvar%2Flib%2Fpostgresql/dbname``.
.. [3] SQLite connects to file based databases. The same URL format is used, omitting
       the hostname, and using the "file" portion as the filename of the database.
       This has the effect of four slashes being present for an absolute file path:
       ``sqlite:////full/path/to/your/database/file.sqlite``.
.. [4] Note that when connecting to Oracle the URL isn't in the form you may know
       from using other Oracle tools (like SQLPlus) i.e. user and password are separated
       by ``:`` not by ``/``. Also you can omit ``HOST`` and ``PORT``
       and provide a full DSN string or TNS name in ``NAME`` part.

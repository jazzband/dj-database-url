# -*- coding: utf-8 -*-
"""
dj-database-url
~~~~~~~~~~~~~~~

.. image:: https://secure.travis-ci.org/kennethreitz/dj-database-url.png?branch=master

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

Support currently exists for PostgreSQL, PostGIS, MySQL and SQLite.

SQLite connects to file based databases. The same URL format is used, omitting
the hostname, and using the "file" portion as the filename of the database.
This has the effect of four slashes being present for an absolute file path:
``sqlite:////full/path/to/your/database/file.sqlite``.


"""

from setuptools import setup

setup(
    name='dj-database-url',
    version='0.4.0',
    url='https://github.com/kennethreitz/dj-database-url',
    license='BSD',
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    description='Use Database URLs in your Django Application.',
    long_description=__doc__,
    py_modules=['dj_database_url'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ]
)

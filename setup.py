# -*- coding: utf-8 -*-
"""
dj-database-url
~~~~~~~~~~~~~~~

This simple Django utility allows you to utilize the
`12factor <http://www.12factor.net/backing-services>`_ inspired
``DATABASE_URL`` environment variable to configure your Django application.


Usage
-----

Configure your database in ``settings.py``::

    DATABASES['default'] = dj_database_url.config()

Nice and simple.

"""

from setuptools import setup

setup(
    name='dj-database-url',
    version='0.1.3',
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

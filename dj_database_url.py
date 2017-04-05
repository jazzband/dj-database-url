# -*- coding: utf-8 -*-

import os
import inspect

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('postgresql')
urlparse.uses_netloc.append('pgsql')
urlparse.uses_netloc.append('postgis')
urlparse.uses_netloc.append('mysql')
urlparse.uses_netloc.append('mysql2')
urlparse.uses_netloc.append('mysqlgis')
urlparse.uses_netloc.append('mysql-connector')
urlparse.uses_netloc.append('spatialite')
urlparse.uses_netloc.append('sqlite')
urlparse.uses_netloc.append('oracle')
urlparse.uses_netloc.append('oraclegis')
urlparse.uses_netloc.append('redshift')

DEFAULT_ENV = 'DATABASE_URL'

SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'pgsql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'mysqlgis': 'django.contrib.gis.db.backends.mysql',
    'mysql-connector': 'mysql.connector.django',
    'spatialite': 'django.contrib.gis.db.backends.spatialite',
    'sqlite': 'django.db.backends.sqlite3',
    'oracle': 'django.db.backends.oracle',
    'oraclegis': 'django.contrib.gis.db.backends.oracle',
    'redshift': 'django_redshift_backend',
}


def config(env=DEFAULT_ENV, default=None, engine=None, conn_max_age=0):
    """Returns configured DATABASE dictionary from DATABASE_URL."""

    if default is None:
        callers_source_filename = inspect.stack()[1][1]
        base_dir = os.path.dirname(os.path.dirname(callers_source_filename))
        db_filename = os.path.join(base_dir, 'db.sqlite3')
        default = "sqlite:///{db_filename}".format(db_filename=db_filename)

    config = {}

    s = os.environ.get(env, default)

    if s:
        config = parse(s, engine, conn_max_age)

    return config


def parse(url, engine=None, conn_max_age=0):
    """Parses a database URL."""

    if url == 'sqlite://:memory:':
        # this is a special case, because if we pass this URL into
        # urlparse, urlparse will choke trying to interpret "memory"
        # as a port number
        return {
            'ENGINE': SCHEMES['sqlite'],
            'NAME': ':memory:'
        }
        # note: no other settings are required for sqlite

    # otherwise parse the url as normal
    config = {}

    url = urlparse.urlparse(url)

    # Split query strings from path.
    path = url.path[1:]
    if '?' in path and not url.query:
        path, query = path.split('?', 2)
    else:
        path, query = path, url.query
    query = urlparse.parse_qs(query)

    # If we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == 'sqlite' and path == '':
        path = ':memory:'

    # Handle postgres percent-encoded paths.
    hostname = url.hostname or ''
    if '%2f' in hostname.lower():
        # Switch to url.netloc to avoid lower cased paths
        hostname = url.netloc
        if "@" in hostname:
            hostname = hostname.rsplit("@", 1)[1]
        if ":" in hostname:
            hostname = hostname.split(":", 1)[0]
        hostname = hostname.replace('%2f', '/').replace('%2F', '/')

    # Update with environment configuration.
    config.update({
        'NAME': urlparse.unquote(path or ''),
        'USER': urlparse.unquote(url.username or ''),
        'PASSWORD': urlparse.unquote(url.password or ''),
        'HOST': hostname,
        'PORT': url.port or '',
        'CONN_MAX_AGE': conn_max_age,
    })

    # Lookup specified engine.
    engine = SCHEMES[url.scheme] if engine is None else engine

    # Pass the query string into OPTIONS.
    options = {}
    for key, values in query.items():
        if url.scheme == 'mysql' and key == 'ssl-ca':
            options['ssl'] = {'ca': values[-1]}
            continue

        options[key] = values[-1]

    # Support for Postgres Schema URLs
    if 'currentSchema' in options and engine in (
        'django.contrib.gis.db.backends.postgis',
        'django.db.backends.postgresql_psycopg2',
        'django_redshift_backend',
    ):
        options['options'] = '-c search_path={0}'.format(options.pop('currentSchema'))

    if options:
        config['OPTIONS'] = options

    if engine:
        config['ENGINE'] = engine

    return config

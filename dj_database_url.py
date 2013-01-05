# -*- coding: utf-8 -*-

import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse



# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('postgresql')
urlparse.uses_netloc.append('postgis')
urlparse.uses_netloc.append('mysql')
urlparse.uses_netloc.append('mysql2')
urlparse.uses_netloc.append('sqlite')

DEFAULT_ENV = 'DATABASE_URL'

SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'sqlite': 'django.db.backends.sqlite3'
}


def config(env=DEFAULT_ENV, default=None):
    """Returns configured DATABASE dictionary from DATABASE_URL."""

    config = {}

    s = os.environ.get(env, default)

    if s:
        config = parse(s)

    return config


def parse(url):
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

    # Remove query strings.
    path = url.path[1:]
    path = path.split('?', 2)[0]

    # if we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == 'sqlite' and path == '':
        path = ':memory:'

    # Update with environment configuration.
    config.update({
        'NAME': path,
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    })

    if url.scheme in SCHEMES:
        config['ENGINE'] = SCHEMES[url.scheme]

    return config

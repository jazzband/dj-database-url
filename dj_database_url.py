# -*- coding: utf-8 -*-

import os
import re

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


class InvalidDatabaseUrl(Exception):
    pass


pattern = re.compile(
        r'^(?P<scheme>(postgres|postgis|mysql|mysqlgis))://'
         '(?P<username>.+?):(?P<password>.+?)@(?P<hostname>.+?):(?P<port>\d+)(?P<path>/.+)')


# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('postgresql')
urlparse.uses_netloc.append('pgsql')
urlparse.uses_netloc.append('postgis')
urlparse.uses_netloc.append('mysql')
urlparse.uses_netloc.append('mysql2')
urlparse.uses_netloc.append('mysqlgis')
urlparse.uses_netloc.append('spatialite')
urlparse.uses_netloc.append('sqlite')

DEFAULT_ENV = 'DATABASE_URL'

SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'pgsql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'mysqlgis': 'django.contrib.gis.db.backends.mysql',
    'spatialite': 'django.contrib.gis.db.backends.spatialite',
    'sqlite': 'django.db.backends.sqlite3',
}



def safe_urlparse(url):
    """if we encounter symbol like '#' use re to parse url"""

    class dictwrapper(dict):
        def __init__(self, d):
            self.__dict__ = d

    match = pattern.search(url)
    if match is None:
        raise InvalidDatabaseUrl(url)
    data = match.groupdict()
    data['port'] = int(data['port'])
    return dictwrapper(data)


def config(env=DEFAULT_ENV, default=None, engine=None):
    """Returns configured DATABASE dictionary from DATABASE_URL."""

    config = {}

    s = os.environ.get(env, default)

    if s:
        config = parse(s, engine)

    return config


def parse(url, engine=None):
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

    if '#' in url:
        url = safe_urlparse(url)
        path = url.path
    else:
        url = urlparse.urlparse(url)

    # Remove query strings.
    path = url.path[1:]
    path = path.split('?', 2)[0]

    # If we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == 'sqlite' and path == '':
        path = ':memory:'

    # Handle postgres percent-encoded paths.
    hostname = url.hostname or ''
    if '%2f' in hostname.lower():
        hostname = hostname.replace('%2f', '/').replace('%2F', '/')

    # Update with environment configuration.
    config.update({
        'NAME': path or '',
        'USER': url.username or '',
        'PASSWORD': url.password or '',
        'HOST': hostname,
        'PORT': url.port or '',
    })

    if engine:
        config['ENGINE'] = engine
    elif url.scheme in SCHEMES:
        config['ENGINE'] = SCHEMES[url.scheme]

    return config

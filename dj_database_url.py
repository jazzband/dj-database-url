# -*- coding: utf-8 -*-

import os
import urlparse

# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mysql')
urlparse.uses_netloc.append('sqlite')

DEFAULT_ENV = 'DATABASE_URL'

def config(env=DEFAULT_ENV, default=None):
    """Returns configured DATABASE dictionary from DATABASE_URL."""

    config = {}

    s = os.environ.get(env, default)

    if s:
        config = parse(s)

    return config


def parse(url):
    """Parses a database URL."""

    config = {}

    url = urlparse.urlparse(url)

    # Update with environment configuration.
    config.update({
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    })

    if url.scheme == 'postgres':
        config['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

    if url.scheme == 'postgis':
        config['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

    if url.scheme == 'mysql':
        config['ENGINE'] = 'django.db.backends.mysql'

    if url.scheme == 'sqlite':
        config['ENGINE'] = 'django.db.backends.sqlite3'

    return config

# -*- coding: utf-8 -*-

import os
import urlparse

# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mysql')

DEFAULT_ENV = 'DATABASE_URL'

def config(env=DEFAULT_ENV):
    """Returns configured DATABASE dictionary from DATABASE_URL."""

    config = {}

    if env in os.environ:
        config = parse(os.environ[env])

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

    if url.scheme == 'mysql':
        config['ENGINE'] = 'django.db.backends.mysql'

    return config
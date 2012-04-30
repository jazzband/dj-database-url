# -*- coding: utf-8 -*-

import os
import urlparse

# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mysql')


def config(config=None):
    """Returns configured DATABASES dictionary."""

    if config is None:
        config = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])

        # Ensure default database exists.
        config.setdefault('default', {})

        # Update with environment configuration.
        config['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })

        if url.scheme == 'postgres':
            config['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

        if url.scheme == 'mysql':
            config['default']['ENGINE'] = 'django.db.backends.mysql'

    return config
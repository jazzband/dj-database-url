# -*- coding: utf-8 -*-

import collections
import os
import urllib.parse as urlparse
import warnings

Engine = collections.namedtuple("Engine", ["backend", "string_ports", "options"])

DEFAULT_ENV = "DATABASE_URL"
ENGINE_SCHEMES = {}


def register(backend, schemes=None, string_ports=False, options=None):
    if schemes is None:
        schemes = [backend.rsplit(".")[-1]]
    elif isinstance(schemes, str):
        schemes = [schemes]

    for scheme in schemes:
        urlparse.uses_netloc.append(scheme)
        ENGINE_SCHEMES[scheme] = Engine(backend, string_ports, options or {})


# Support all the first-party Django engines out of the box.
register(
    "django.db.backends.postgresql",
    ("postgres", "postgresql", "pgsql"),
    options={
        "currentSchema": lambda values: {
            "options": "-c search_path={}".format(values[-1])
        },
    },
)
register(
    "django.contrib.gis.db.backends.postgis",
    options={
        "currentSchema": lambda values: {
            "options": "-c search_path={}".format(values[-1])
        },
    },
)
register("django.contrib.gis.db.backends.spatialite")
register(
    "django.db.backends.mysql",
    options={
        "ssl-ca": lambda values: {"ssl": {"ca": values[-1]}},
    },
)
register("django.contrib.gis.db.backends.mysql", "mysqlgis")
register("django.db.backends.oracle", string_ports=True)
register("django.contrib.gis.db.backends.oracle", "oraclegis")
register("django.db.backends.sqlite3", "sqlite")


def config(env=DEFAULT_ENV, default=None, **settings):
    """Returns configured DATABASE dictionary from DATABASE_URL."""

    s = os.environ.get(env, default)
    return parse(s, **settings) if s else {}


def parse(url, backend=None, **settings):
    """Parses a database URL."""

    if url == "sqlite://:memory:":
        # this is a special case, because if we pass this URL into
        # urlparse, urlparse will choke trying to interpret "memory"
        # as a port number
        return {"ENGINE": ENGINE_SCHEMES["sqlite"].backend, "NAME": ":memory:"}
        # note: no other settings are required for sqlite

    url = urlparse.urlparse(url)
    engine = ENGINE_SCHEMES[url.scheme]
    options = {}

    if "engine" in settings:
        # Keep compatibility with dj-database-url for `engine` kwarg.
        backend = settings.pop("engine")

    if "conn_max_age" in settings:
        warnings.warn(
            "The `conn_max_age` argument is deprecated. Use `CONN_MAX_AGE` instead."
        )
        settings["CONN_MAX_AGE"] = settings.pop("conn_max_age")

    if "ssl_require" in settings:
        warnings.warn(
            "The `ssl_require` argument is deprecated. "
            "Use `OPTIONS={'sslmode': 'require'}` instead."
        )
        if settings.pop("ssl_require"):
            options["sslmode"] = "require"

    # Split query strings from path.
    path = url.path[1:]
    if "?" in path and not url.query:
        path, query = path.split("?", 1)
    else:
        path, query = path, url.query
    query = urlparse.parse_qs(query)

    # If we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == "sqlite" and path == "":
        path = ":memory:"

    # Handle postgres percent-encoded paths.
    hostname = url.hostname or ""
    if "%2f" in hostname.lower():
        # Switch to url.netloc to avoid lower cased paths
        hostname = url.netloc
        if "@" in hostname:
            hostname = hostname.rsplit("@", 1)[1]
        if ":" in hostname:
            hostname = hostname.split(":", 1)[0]
        hostname = hostname.replace("%2f", "/").replace("%2F", "/")

    port = str(url.port) if url.port and engine.string_ports else url.port

    # Pass the query string into OPTIONS.
    for key, values in query.items():
        if key in engine.options:
            options.update(engine.options[key](values))
        else:
            options[key] = values[-1]

    # Allow passed OPTIONS to override query string options.
    options.update(settings.pop("OPTIONS", {}))

    # Update with environment configuration.
    config = {
        "ENGINE": backend or engine.backend,
        "NAME": urlparse.unquote(path or ""),
        "USER": urlparse.unquote(url.username or ""),
        "PASSWORD": urlparse.unquote(url.password or ""),
        "HOST": hostname,
        "PORT": port or "",
    }

    if options:
        config["OPTIONS"] = options

    # Update the final config with any settings passed in explicitly.
    config.update(**settings)

    return config

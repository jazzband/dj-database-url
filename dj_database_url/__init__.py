import logging
import os
import string
import urllib.parse as urlparse
from typing import Any, Dict, Optional, Union

from typing_extensions import TypedDict

DEFAULT_ENV = "DATABASE_URL"

SCHEMES = {
    "postgres": "django.db.backends.postgresql",
    "postgresql": "django.db.backends.postgresql",
    "pgsql": "django.db.backends.postgresql",
    "postgis": "django.contrib.gis.db.backends.postgis",
    "mysql": "django.db.backends.mysql",
    "mysql2": "django.db.backends.mysql",
    "mysqlgis": "django.contrib.gis.db.backends.mysql",
    "mysql-connector": "mysql.connector.django",
    "mssql": "sql_server.pyodbc",
    "mssqlms": "mssql",
    "spatialite": "django.contrib.gis.db.backends.spatialite",
    "sqlite": "django.db.backends.sqlite3",
    "oracle": "django.db.backends.oracle",
    "oraclegis": "django.contrib.gis.db.backends.oracle",
    "redshift": "django_redshift_backend",
    "cockroach": "django_cockroachdb",
    "timescale": "timescale.db.backends.postgresql",
    "timescalegis": "timescale.db.backends.postgis",
}

QUERY_STRING_OPTIONS_OVERLAP_ERROR = (
    "Query string options and options cannot overlap. "
    "Query string options: $query_string_options. "
    "Options: $options"
)

# Register database schemes in URLs.
for key in SCHEMES.keys():
    urlparse.uses_netloc.append(key)


# From https://docs.djangoproject.com/en/4.0/ref/settings/#databases
class DBConfig(TypedDict, total=False):
    ATOMIC_REQUESTS: bool
    AUTOCOMMIT: bool
    CONN_MAX_AGE: Optional[int]
    CONN_HEALTH_CHECKS: bool
    DISABLE_SERVER_SIDE_CURSORS: bool
    ENGINE: str
    HOST: str
    NAME: str
    OPTIONS: Optional[Dict[str, Any]]
    PASSWORD: str
    PORT: Union[str, int]
    TEST: Dict[str, Any]
    TIME_ZONE: str
    USER: str


def config(
    env: str = DEFAULT_ENV,
    default: Optional[str] = None,
    engine: Optional[str] = None,
    conn_max_age: Optional[int] = 0,
    conn_health_checks: bool = False,
    ssl_require: bool = False,
    test_options: Optional[Dict] = None,
    options: Optional[Dict] = None,
) -> DBConfig:
    """Returns configured DATABASE dictionary from DATABASE_URL."""
    s = os.environ.get(env, default)

    if s is None:
        logging.warning(
            "No %s environment variable set, and so no databases setup" % env
        )

    if s:
        return parse(
            url=s,
            engine=engine,
            conn_max_age=conn_max_age,
            conn_health_checks=conn_health_checks,
            ssl_require=ssl_require,
            test_options=test_options,
            options=options,
        )

    return {}


def parse(
    url: str,
    engine: Optional[str] = None,
    conn_max_age: Optional[int] = 0,
    conn_health_checks: bool = False,
    ssl_require: bool = False,
    test_options: Optional[dict] = None,
    options: Optional[Dict] = None,
) -> DBConfig:
    """Parses a database URL."""
    if url == "sqlite://:memory:":
        # this is a special case, because if we pass this URL into
        # urlparse, urlparse will choke trying to interpret "memory"
        # as a port number
        return {"ENGINE": SCHEMES["sqlite"], "NAME": ":memory:"}
        # note: no other settings are required for sqlite

    # otherwise parse the url as normal
    parsed_config: DBConfig = {}

    if test_options is None:
        test_options = {}

    if options is None:
        options = {}

    spliturl = urlparse.urlsplit(url)

    # Split query strings from path.
    path = spliturl.path[1:]
    query = urlparse.parse_qs(spliturl.query)

    # If we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if spliturl.scheme == "sqlite" and path == "":
        path = ":memory:"

    # Handle postgres percent-encoded paths.
    hostname = spliturl.hostname or ""
    if "%" in hostname:
        # Switch to url.netloc to avoid lower cased paths
        hostname = spliturl.netloc
        if "@" in hostname:
            hostname = hostname.rsplit("@", 1)[1]
        # Use URL Parse library to decode % encodes
        hostname = urlparse.unquote(hostname)

    # Lookup specified engine.
    if engine is None:
        engine = SCHEMES.get(spliturl.scheme)
        if engine is None:
            raise ValueError(
                "No support for '%s'. We support: %s"
                % (spliturl.scheme, ", ".join(sorted(SCHEMES.keys())))
            )

    port = (
        str(spliturl.port)
        if spliturl.port
        and engine in (SCHEMES["oracle"], SCHEMES["mssql"], SCHEMES["mssqlms"])
        else spliturl.port
    )

    # Update with environment configuration.
    parsed_config.update(
        {
            "NAME": urlparse.unquote(path or ""),
            "USER": urlparse.unquote(spliturl.username or ""),
            "PASSWORD": urlparse.unquote(spliturl.password or ""),
            "HOST": hostname,
            "PORT": port or "",
            "CONN_MAX_AGE": conn_max_age,
            "CONN_HEALTH_CHECKS": conn_health_checks,
            "ENGINE": engine,
        }
    )
    if test_options:
        parsed_config.update(
            {
                'TEST': test_options,
            }
        )

    # Pass the query string into OPTIONS.
    query_string_options: Dict[str, Any] = {}
    for key, values in query.items():
        if spliturl.scheme == "mysql" and key == "ssl-ca":
            query_string_options["ssl"] = {"ca": values[-1]}
            continue

        query_string_options[key] = values[-1]

    if ssl_require:
        query_string_options["sslmode"] = "require"

    # Support for Postgres Schema URLs
    if "currentSchema" in query_string_options and engine in (
        "django.contrib.gis.db.backends.postgis",
        "django.db.backends.postgresql_psycopg2",
        "django.db.backends.postgresql",
        "django_redshift_backend",
        "timescale.db.backends.postgresql",
        "timescale.db.backends.postgis",
    ):
        query_string_options["options"] = "-c search_path={0}".format(
            query_string_options.pop("currentSchema")
        )

    if query_string_options:
        parsed_config["OPTIONS"] = query_string_options

    check_if_query_string_options_overlaps_options(
        query_string_options=query_string_options, options=options
    )

    if options:
        parsed_config["OPTIONS"] = options

    return parsed_config


def check_if_query_string_options_overlaps_options(
    query_string_options: Dict[str, Any], options: Dict[str, Any]
) -> None:
    # Some query options automatically set the OPTIONS key. To maintain support
    # and not have users accidentally wondering what broke their config. We raise
    # a ValueError when values overlap.
    query_string_options_set = set(query_string_options.keys())
    options_set = set(options.keys())

    if query_string_options_set & options_set:
        query_string_options_selected = ', '.join(query_string_options_set)
        options_selected = ', '.join(options_set)
        message = string.Template(QUERY_STRING_OPTIONS_OVERLAP_ERROR).substitute(
            query_string_options=query_string_options_selected, options=options_selected
        )
        raise ValueError(message)

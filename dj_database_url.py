import os
import urllib.parse as urlparse
from typing import Any, Dict, Optional, Union, Sequence

# Support Python 3.7.
# `try: from typing import Literal` causes:
# error: Module 'typing' has no attribute 'Literal'  [attr-defined]
from typing_extensions import TypedDict, Literal

# Register database schemes in URLs.
urlparse.uses_netloc.append("postgres")
urlparse.uses_netloc.append("postgresql")
urlparse.uses_netloc.append("pgsql")
urlparse.uses_netloc.append("postgis")
urlparse.uses_netloc.append("mysql")
urlparse.uses_netloc.append("mysql2")
urlparse.uses_netloc.append("mysqlgis")
urlparse.uses_netloc.append("mysql-connector")
urlparse.uses_netloc.append("mssql")
urlparse.uses_netloc.append("mssqlms")
urlparse.uses_netloc.append("spatialite")
urlparse.uses_netloc.append("sqlite")
urlparse.uses_netloc.append("oracle")
urlparse.uses_netloc.append("oraclegis")
urlparse.uses_netloc.append("redshift")
urlparse.uses_netloc.append("cockroach")
urlparse.uses_netloc.append("timescale")
urlparse.uses_netloc.append("timescalegis")
urlparse.uses_netloc.append("mongodb")
urlparse.uses_netloc.append("mongodb+srv")

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
    "mongodb": "djongo",
    "mongodb+srv": "djongo",
}


# From https://docs.djangoproject.com/en/4.0/ref/settings/#databases
class DBConfig(TypedDict, total=False):
    ATOMIC_REQUESTS: bool
    AUTOCOMMIT: bool
    CONN_MAX_AGE: int
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
    # MongoDB (djongo backend):
    CLIENT: Optional[Dict[str, Any]]
    ENFORCE_SCHEMA: bool


def config(
    env: str = DEFAULT_ENV,
    default: Optional[str] = None,
    engine: Optional[str] = None,
    conn_max_age: int = 0,
    conn_health_checks: bool = False,
    ssl_require: bool = False,
    test_options: Optional[Dict] = None,
) -> DBConfig:
    """Returns configured DATABASE dictionary from DATABASE_URL."""
    s = os.environ.get(env, default)

    if s:
        return parse(
            s, engine, conn_max_age, conn_health_checks, ssl_require, test_options
        )

    return {}


def parse(
    url: str,
    engine: Optional[str] = None,
    conn_max_age: int = 0,
    conn_health_checks: bool = False,
    ssl_require: bool = False,
    test_options: Optional[dict] = None,
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

    spliturl = urlparse.urlsplit(url)

    # Split query strings from path.
    path = spliturl.path[1:]
    if "?" in path and not spliturl.query:
        path, raw_query = path.split("?", 2)
    else:
        path, raw_query = path, spliturl.query
    query = urlparse.parse_qs(raw_query)

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
        if ":" in hostname:
            hostname = hostname.split(":", 1)[0]
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

    try:
        port = (
            str(spliturl.port)
            if spliturl.port
            and engine in (SCHEMES["oracle"], SCHEMES["mssql"], SCHEMES["mssqlms"])
            else spliturl.port
        )
    except Exception as e:
        if engine == "djongo":  # compatible with multiple host:port
            port = None
        else:
            raise e

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
        }
    )
    if test_options:
        parsed_config.update(
            {'TEST': test_options,}
        )

    # Pass the query string into OPTIONS.
    options: Dict[str, Any] = {}
    for key, values in query.items():
        if spliturl.scheme == "mysql" and key == "ssl-ca":
            options["ssl"] = {"ca": values[-1]}
            continue

        options[key] = values[-1]

    if ssl_require:
        options["sslmode"] = "require"

    # Support for Postgres Schema URLs
    if "currentSchema" in options and engine in (
        "django.contrib.gis.db.backends.postgis",
        "django.db.backends.postgresql_psycopg2",
        "django.db.backends.postgresql",
        "django_redshift_backend",
        "timescale.db.backends.postgresql",
        "timescale.db.backends.postgis",
    ):
        options["options"] = "-c search_path={0}".format(options.pop("currentSchema"))

    if options:
        parsed_config["OPTIONS"] = options

    if engine:
        parsed_config["ENGINE"] = engine

    # MongoDB
    if engine == "djongo":
        if "enforceSchema" in options:
            # Remove the enforceSchema option from the options dict
            parsed_config["ENFORCE_SCHEMA"] = (
                options.pop("enforceSchema").lower() == "true"
            )

        if spliturl.query == "":
            host = url
        else:
            host = f"{url.split('?')[0]}?{urlparse.urlencode(options)}"
        parsed_config["CLIENT"] = {"host": host}

        # default database
        if parsed_config['NAME'] == '':
            parsed_config['NAME'] = 'db'

        # pop unnecessary options
        remove_key_list: Sequence[
            Literal['USER', 'PASSWORD', 'HOST', 'PORT', 'OPTIONS']
        ] = [
            'USER',
            'PASSWORD',
            'HOST',
            'PORT',
            'OPTIONS',
        ]  # cannot use list[str] directly:
        # https://github.com/python/mypy/issues/7178#issuecomment-1208364397

        for key in remove_key_list:
            if key in parsed_config:
                parsed_config.pop(key)

    return parsed_config

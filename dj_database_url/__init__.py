import logging
import os
import urllib.parse as urlparse
from typing import Any, Callable, Dict, List, Optional, TypedDict, Union

DEFAULT_ENV = "DATABASE_URL"
ENGINE_SCHEMES: Dict[str, "Engine"] = {}


# From https://docs.djangoproject.com/en/stable/ref/settings/#databases
class DBConfig(TypedDict, total=False):
    ATOMIC_REQUESTS: bool
    AUTOCOMMIT: bool
    CONN_MAX_AGE: Optional[int]
    CONN_HEALTH_CHECKS: bool
    DISABLE_SERVER_SIDE_CURSORS: bool
    ENGINE: str
    HOST: str
    NAME: str
    OPTIONS: Dict[str, Any]
    PASSWORD: str
    PORT: Union[str, int]
    TEST: Dict[str, Any]
    TIME_ZONE: str
    USER: str


PostprocessCallable = Callable[[DBConfig], None]
OptionType = Union[int, str, bool]


class ParseError(ValueError):
    def __str__(self) -> str:
        return (
            "This string is not a valid url, possibly because some of its parts"
            " is not properly urllib.parse.quote()'ed."
        )


class UnknownSchemeError(ValueError):
    def __init__(self, scheme: str) -> None:
        self.scheme = scheme

    def __str__(self) -> str:
        schemes = ", ".join(sorted(ENGINE_SCHEMES.keys()))
        return (
            f"Scheme '{self.scheme}://' is unknown."
            " Did you forget to register custom backend?"
            f" Following schemes have registered backends: {schemes}."
        )


def default_postprocess(parsed_config: DBConfig) -> None:
    pass


class Engine:
    def __init__(
        self,
        backend: str,
        postprocess: PostprocessCallable = default_postprocess,
    ) -> None:
        self.backend = backend
        self.postprocess = postprocess


def register(
    scheme: str, backend: str
) -> Callable[[PostprocessCallable], PostprocessCallable]:
    engine = Engine(backend)
    if scheme not in ENGINE_SCHEMES:
        urlparse.uses_netloc.append(scheme)
    ENGINE_SCHEMES[scheme] = engine

    def inner(func: PostprocessCallable) -> PostprocessCallable:
        engine.postprocess = func
        return func

    return inner


register("spatialite", "django.contrib.gis.db.backends.spatialite")
register("mysql-connector", "mysql.connector.django")
register("mysqlgis", "django.contrib.gis.db.backends.mysql")
register("oraclegis", "django.contrib.gis.db.backends.oracle")
register("cockroach", "django_cockroachdb")


@register("sqlite", "django.db.backends.sqlite3")
def default_to_in_memory_db(parsed_config: DBConfig) -> None:
    # mimic sqlalchemy behaviour
    if not parsed_config.get("NAME"):
        parsed_config["NAME"] = ":memory:"


@register("oracle", "django.db.backends.oracle")
@register("mssqlms", "mssql")
@register("mssql", "sql_server.pyodbc")
def stringify_port(parsed_config: DBConfig) -> None:
    parsed_config["PORT"] = str(parsed_config.get("PORT", ""))


@register("mysql", "django.db.backends.mysql")
@register("mysql2", "django.db.backends.mysql")
def apply_ssl_ca(parsed_config: DBConfig) -> None:
    options = parsed_config.get("OPTIONS", {})
    ca = options.pop("ssl-ca", None)
    if ca:
        options["ssl"] = {"ca": ca}


@register("postgres", "django.db.backends.postgresql")
@register("postgresql", "django.db.backends.postgresql")
@register("pgsql", "django.db.backends.postgresql")
@register("postgis", "django.contrib.gis.db.backends.postgis")
@register("redshift", "django_redshift_backend")
@register("timescale", "timescale.db.backends.postgresql")
@register("timescalegis", "timescale.db.backends.postgis")
def apply_current_schema(parsed_config: DBConfig) -> None:
    options = parsed_config.get("OPTIONS", {})
    schema = options.pop("currentSchema", None)
    if schema:
        options["options"] = f"-c search_path={schema}"


def config(
    env: str = DEFAULT_ENV,
    default: Optional[str] = None,
    engine: Optional[str] = None,
    conn_max_age: int = 0,
    conn_health_checks: bool = False,
    disable_server_side_cursors: bool = False,
    ssl_require: bool = False,
    test_options: Optional[Dict[str, Any]] = None,
) -> DBConfig:
    """Returns configured DATABASE dictionary from DATABASE_URL."""
    s = os.environ.get(env, default)

    if s is None:
        logging.warning(
            "No %s environment variable set, and so no databases setup", env
        )

    if s:
        return parse(
            s,
            engine,
            conn_max_age,
            conn_health_checks,
            disable_server_side_cursors,
            ssl_require,
            test_options,
        )

    return {}


def parse(
    url: str,
    engine: Optional[str] = None,
    conn_max_age: int = 0,
    conn_health_checks: bool = False,
    disable_server_side_cursors: bool = False,
    ssl_require: bool = False,
    test_options: Optional[Dict[str, Any]] = None,
) -> DBConfig:
    """Parses a database URL and returns configured DATABASE dictionary."""
    settings = _convert_to_settings(
        engine,
        conn_max_age,
        conn_health_checks,
        disable_server_side_cursors,
        ssl_require,
        test_options,
    )

    if url == "sqlite://:memory:":
        # this is a special case, because if we pass this URL into
        # urlparse, urlparse will choke trying to interpret "memory"
        # as a port number
        return {"ENGINE": ENGINE_SCHEMES["sqlite"].backend, "NAME": ":memory:"}
        # note: no other settings are required for sqlite

    try:
        split_result = urlparse.urlsplit(url)
        engine_obj = ENGINE_SCHEMES.get(split_result.scheme)
        if engine_obj is None:
            raise UnknownSchemeError(split_result.scheme)
        path = split_result.path[1:]
        query = urlparse.parse_qs(split_result.query)
        options = {k: _parse_option_values(v) for k, v in query.items()}
        parsed_config: DBConfig = {
            "ENGINE": engine_obj.backend,
            "USER": urlparse.unquote(split_result.username or ""),
            "PASSWORD": urlparse.unquote(split_result.password or ""),
            "HOST": urlparse.unquote(split_result.hostname or ""),
            "PORT": split_result.port or "",
            "NAME": urlparse.unquote(path),
            "OPTIONS": options,
        }
    except UnknownSchemeError:
        raise
    except ValueError:
        raise ParseError() from None

    # Guarantee that config has options, possibly empty, when postprocess() is called
    assert isinstance(parsed_config["OPTIONS"], dict)
    engine_obj.postprocess(parsed_config)

    # Update the final config with any settings passed in explicitly.
    parsed_config["OPTIONS"].update(settings.pop("OPTIONS", {}))
    parsed_config.update(settings)

    if not parsed_config["OPTIONS"]:
        parsed_config.pop("OPTIONS")
    return parsed_config


def _parse_option_values(values: List[str]) -> Union[OptionType, List[OptionType]]:
    parsed_values = [_parse_value(v) for v in values]
    return parsed_values[0] if len(parsed_values) == 1 else parsed_values


def _parse_value(value: str) -> OptionType:
    if value.isdigit():
        return int(value)
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    return value


def _convert_to_settings(
    engine: Optional[str],
    conn_max_age: int,
    conn_health_checks: bool,
    disable_server_side_cursors: bool,
    ssl_require: bool,
    test_options: Optional[dict[str, Any]],
) -> DBConfig:
    settings: DBConfig = {
        "CONN_MAX_AGE": conn_max_age,
        "CONN_HEALTH_CHECKS": conn_health_checks,
        "DISABLE_SERVER_SIDE_CURSORS": disable_server_side_cursors,
    }
    if engine:
        settings["ENGINE"] = engine
    if ssl_require:
        settings["OPTIONS"] = {}
        settings["OPTIONS"]["sslmode"] = "require"
    if test_options:
        settings["TEST"] = test_options
    return settings

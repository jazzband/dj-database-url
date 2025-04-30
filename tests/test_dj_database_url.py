# pyright: reportTypedDictNotRequiredAccess=false

import os
import re
import unittest
from unittest import mock
from urllib.parse import uses_netloc

import dj_database_url

POSTGIS_URL = "postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn"


class DatabaseTestSuite(unittest.TestCase):
    def test_postgres_parsing(self) -> None:
        url = dj_database_url.parse(
            "postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_postgres_unix_socket_parsing(self) -> None:
        url = dj_database_url.parse(
            "postgres://%2Fvar%2Frun%2Fpostgresql/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "/var/run/postgresql"
        assert url["USER"] == ""
        assert url["PASSWORD"] == ""
        assert url["PORT"] == ""

        url = dj_database_url.parse(
            "postgres://%2FUsers%2Fpostgres%2FRuN/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["HOST"] == "/Users/postgres/RuN"
        assert url["USER"] == ""
        assert url["PASSWORD"] == ""
        assert url["PORT"] == ""

    def test_postgres_google_cloud_parsing(self) -> None:
        url = dj_database_url.parse(
            "postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@%2Fcloudsql%2Fproject_id%3Aregion%3Ainstance_id/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "/cloudsql/project_id:region:instance_id"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == ""

    def test_ipv6_parsing(self) -> None:
        url = dj_database_url.parse(
            "postgres://ieRaekei9wilaim7:wegauwhgeuioweg@[2001:db8:1234::1234:5678:90af]:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "2001:db8:1234::1234:5678:90af"
        assert url["USER"] == "ieRaekei9wilaim7"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_postgres_search_path_parsing(self) -> None:
        url = dj_database_url.parse(
            "postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?currentSchema=otherschema"
        )
        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431
        assert url["OPTIONS"]["options"] == "-c search_path=otherschema"
        assert "currentSchema" not in url["OPTIONS"]

    def test_postgres_parsing_with_special_characters(self) -> None:
        url = dj_database_url.parse(
            "postgres://%23user:%23password@ec2-107-21-253-135.compute-1.amazonaws.com:5431/%23database"
        )

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "#database"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "#user"
        assert url["PASSWORD"] == "#password"
        assert url["PORT"] == 5431

    def test_postgres_parsing_with_int_bool_str_query_string(self) -> None:
        url = dj_database_url.parse(
            "postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?server_side_binding=true&timeout=20&service=my_service&passfile=.my_pgpass"
        )

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431
        assert url["OPTIONS"]["server_side_binding"] is True
        assert url["OPTIONS"]["timeout"] == 20
        assert url["OPTIONS"]["service"] == "my_service"
        assert url["OPTIONS"]["passfile"] == ".my_pgpass"

    def test_postgis_parsing(self) -> None:
        url = dj_database_url.parse(
            "postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "django.contrib.gis.db.backends.postgis"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_postgis_search_path_parsing(self) -> None:
        url = dj_database_url.parse(
            "postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?currentSchema=otherschema"
        )
        assert url["ENGINE"] == "django.contrib.gis.db.backends.postgis"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431
        assert url["OPTIONS"]["options"] == "-c search_path=otherschema"
        assert "currentSchema" not in url["OPTIONS"]

    def test_mysql_gis_parsing(self) -> None:
        url = dj_database_url.parse(
            "mysqlgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "django.contrib.gis.db.backends.mysql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_mysql_connector_parsing(self) -> None:
        url = dj_database_url.parse(
            "mysql-connector://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "mysql.connector.django"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_config_test_options(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_URL": "postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?"
            },
        ):
            test_db_config = {
                'NAME': 'mytestdatabase',
            }
            url = dj_database_url.config(test_options=test_db_config)

        assert url['TEST']['NAME'] == 'mytestdatabase'

    def test_cleardb_parsing(self) -> None:
        url = dj_database_url.parse(
            "mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true"
        )

        assert url["ENGINE"] == "django.db.backends.mysql"
        assert url["NAME"] == "heroku_97681db3eff7580"
        assert url["HOST"] == "us-cdbr-east.cleardb.com"
        assert url["USER"] == "bea6eb025ca0d8"
        assert url["PASSWORD"] == "69772142"
        assert url["PORT"] == ""

    def test_database_url(self) -> None:
        with mock.patch.dict(os.environ, clear=True):
            a = dj_database_url.config()
        assert not a

        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_URL": "postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn"
            },
        ):
            url = dj_database_url.config()

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_empty_sqlite_url(self) -> None:
        url = dj_database_url.parse("sqlite://")

        assert url["ENGINE"] == "django.db.backends.sqlite3"
        assert url["NAME"] == ":memory:"

    def test_memory_sqlite_url(self) -> None:
        url = dj_database_url.parse("sqlite://:memory:")

        assert url["ENGINE"] == "django.db.backends.sqlite3"
        assert url["NAME"] == ":memory:"

    def test_sqlite_relative_url(self) -> None:
        url = "sqlite:///db.sqlite3"
        config = dj_database_url.parse(url)

        assert config["ENGINE"] == "django.db.backends.sqlite3"
        assert config["NAME"] == "db.sqlite3"

    def test_sqlite_absolute_url(self) -> None:
        # 4 slashes are needed:
        # two are part of scheme
        # one separates host:port from path
        # and the fourth goes to "NAME" value
        url = "sqlite:////db.sqlite3"
        config = dj_database_url.parse(url)

        assert config["ENGINE"] == "django.db.backends.sqlite3"
        assert config["NAME"] == "/db.sqlite3"

    def test_parse_engine_setting(self) -> None:
        engine = "django_mysqlpool.backends.mysqlpool"
        url = dj_database_url.parse(
            "mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true",
            engine,
        )

        assert url["ENGINE"] == engine

    def test_config_engine_setting(self) -> None:
        engine = "django_mysqlpool.backends.mysqlpool"
        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_URL": "mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true"
            },
        ):
            url = dj_database_url.config(engine=engine)

        assert url["ENGINE"] == engine

    def test_parse_conn_max_age_setting(self) -> None:
        conn_max_age = 600
        url = dj_database_url.parse(
            "mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true",
            conn_max_age=conn_max_age,
        )

        assert url["CONN_MAX_AGE"] == conn_max_age

    def test_config_conn_max_age_setting(self) -> None:
        conn_max_age = 600
        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_URL": "mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true"
            },
        ):
            url = dj_database_url.config(conn_max_age=conn_max_age)

        assert url["CONN_MAX_AGE"] == conn_max_age

    def test_database_url_with_options(self) -> None:
        # Test full options
        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_URL": "postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?sslrootcert=rds-combined-ca-bundle.pem&sslmode=verify-full"
            },
        ):
            url = dj_database_url.config()

        assert url["ENGINE"] == "django.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431
        assert url["OPTIONS"] == {
            "sslrootcert": "rds-combined-ca-bundle.pem",
            "sslmode": "verify-full",
        }

        # Test empty options
        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_URL": "postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?"
            },
        ):
            url = dj_database_url.config()
        assert "OPTIONS" not in url

    def test_mysql_database_url_with_sslca_options(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_URL": "mysql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:3306/d8r82722r2kuvn?ssl-ca=rds-combined-ca-bundle.pem"
            },
        ):
            url = dj_database_url.config()

        assert url["ENGINE"] == "django.db.backends.mysql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 3306
        assert url["OPTIONS"] == {"ssl": {"ca": "rds-combined-ca-bundle.pem"}}

        # Test empty options
        with mock.patch.dict(
            os.environ,
            {
                "DATABASE_URL": "mysql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:3306/d8r82722r2kuvn?"
            },
        ):
            url = dj_database_url.config()
        assert "OPTIONS" not in url

    def test_oracle_parsing(self) -> None:
        url = dj_database_url.parse("oracle://scott:tiger@oraclehost:1521/hr")

        assert url["ENGINE"] == "django.db.backends.oracle"
        assert url["NAME"] == "hr"
        assert url["HOST"] == "oraclehost"
        assert url["USER"] == "scott"
        assert url["PASSWORD"] == "tiger"
        assert url["PORT"] == "1521"

    def test_oracle_gis_parsing(self) -> None:
        url = dj_database_url.parse("oraclegis://scott:tiger@oraclehost:1521/hr")

        assert url["ENGINE"] == "django.contrib.gis.db.backends.oracle"
        assert url["NAME"] == "hr"
        assert url["HOST"] == "oraclehost"
        assert url["USER"] == "scott"
        assert url["PASSWORD"] == "tiger"
        assert url["PORT"] == 1521

    def test_oracle_dsn_parsing(self) -> None:
        url = dj_database_url.parse(
            "oracle://scott:tiger@/"
            "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)"
            "(HOST=oraclehost)(PORT=1521)))"
            "(CONNECT_DATA=(SID=hr)))"
        )

        assert url["ENGINE"] == "django.db.backends.oracle"
        assert url["USER"] == "scott"
        assert url["PASSWORD"] == "tiger"
        assert url["HOST"] == ""
        assert url["PORT"] == ""

        dsn = (
            "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)"
            "(HOST=oraclehost)(PORT=1521)))"
            "(CONNECT_DATA=(SID=hr)))"
        )

        assert url["NAME"] == dsn

    def test_oracle_tns_parsing(self) -> None:
        url = dj_database_url.parse("oracle://scott:tiger@/tnsname")

        assert url["ENGINE"] == "django.db.backends.oracle"
        assert url["USER"] == "scott"
        assert url["PASSWORD"] == "tiger"
        assert url["NAME"] == "tnsname"
        assert url["HOST"] == ""
        assert url["PORT"] == ""

    def test_redshift_parsing(self) -> None:
        url = dj_database_url.parse(
            "redshift://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5439/d8r82722r2kuvn?currentSchema=otherschema"
        )

        assert url["ENGINE"] == "django_redshift_backend"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5439
        assert url["OPTIONS"]["options"] == "-c search_path=otherschema"
        assert "currentSchema" not in url["OPTIONS"]

    def test_mssql_parsing(self) -> None:
        url = dj_database_url.parse(
            "mssql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com/d8r82722r2kuvn?driver=ODBC Driver 13 for SQL Server"
        )

        assert url["ENGINE"] == "sql_server.pyodbc"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == ""
        assert url["OPTIONS"]["driver"] == "ODBC Driver 13 for SQL Server"
        assert "currentSchema" not in url["OPTIONS"]

    def test_mssql_instance_port_parsing(self) -> None:
        url = dj_database_url.parse(
            "mssql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com\\insnsnss:12345/d8r82722r2kuvn?driver=ODBC Driver 13 for SQL Server"
        )

        assert url["ENGINE"] == "sql_server.pyodbc"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com\\insnsnss"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == "12345"
        assert url["OPTIONS"]["driver"] == "ODBC Driver 13 for SQL Server"
        assert "currentSchema" not in url["OPTIONS"]

    def test_cockroach(self) -> None:
        url = dj_database_url.parse(
            "cockroach://testuser:testpass@testhost:26257/cockroach?sslmode=verify-full&sslrootcert=/certs/ca.crt&sslcert=/certs/client.myprojectuser.crt&sslkey=/certs/client.myprojectuser.key"
        )
        assert url['ENGINE'] == 'django_cockroachdb'
        assert url['NAME'] == 'cockroach'
        assert url['HOST'] == 'testhost'
        assert url['USER'] == 'testuser'
        assert url['PASSWORD'] == 'testpass'
        assert url['PORT'] == 26257
        assert url['OPTIONS']['sslmode'] == 'verify-full'
        assert url['OPTIONS']['sslrootcert'] == '/certs/ca.crt'
        assert url['OPTIONS']['sslcert'] == '/certs/client.myprojectuser.crt'
        assert url['OPTIONS']['sslkey'] == '/certs/client.myprojectuser.key'

    def test_mssqlms_parsing(self) -> None:
        url = dj_database_url.parse(
            "mssqlms://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com/d8r82722r2kuvn?driver=ODBC Driver 13 for SQL Server"
        )

        assert url["ENGINE"] == "mssql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == ""
        assert url["OPTIONS"]["driver"] == "ODBC Driver 13 for SQL Server"
        assert "currentSchema" not in url["OPTIONS"]

    def test_timescale_parsing(self) -> None:
        url = dj_database_url.parse(
            "timescale://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_timescale_unix_socket_parsing(self) -> None:
        url = dj_database_url.parse(
            "timescale://%2Fvar%2Frun%2Fpostgresql/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "/var/run/postgresql"
        assert url["USER"] == ""
        assert url["PASSWORD"] == ""
        assert url["PORT"] == ""

        url = dj_database_url.parse(
            "timescale://%2FUsers%2Fpostgres%2FRuN/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgresql"
        assert url["HOST"] == "/Users/postgres/RuN"
        assert url["USER"] == ""
        assert url["PASSWORD"] == ""
        assert url["PORT"] == ""

    def test_timescale_ipv6_parsing(self) -> None:
        url = dj_database_url.parse(
            "timescale://ieRaekei9wilaim7:wegauwhgeuioweg@[2001:db8:1234::1234:5678:90af]:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "2001:db8:1234::1234:5678:90af"
        assert url["USER"] == "ieRaekei9wilaim7"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_timescale_search_path_parsing(self) -> None:
        url = dj_database_url.parse(
            "timescale://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?currentSchema=otherschema"
        )
        assert url["ENGINE"] == "timescale.db.backends.postgresql"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431
        assert url["OPTIONS"]["options"] == "-c search_path=otherschema"
        assert "currentSchema" not in url["OPTIONS"]

    def test_timescale_parsing_with_special_characters(self) -> None:
        url = dj_database_url.parse(
            "timescale://%23user:%23password@ec2-107-21-253-135.compute-1.amazonaws.com:5431/%23database"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgresql"
        assert url["NAME"] == "#database"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "#user"
        assert url["PASSWORD"] == "#password"
        assert url["PORT"] == 5431

    def test_timescalegis_parsing(self) -> None:
        url = dj_database_url.parse(
            "timescalegis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgis"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_timescalegis_unix_socket_parsing(self) -> None:
        url = dj_database_url.parse(
            "timescalegis://%2Fvar%2Frun%2Fpostgresql/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgis"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "/var/run/postgresql"
        assert url["USER"] == ""
        assert url["PASSWORD"] == ""
        assert url["PORT"] == ""

        url = dj_database_url.parse(
            "timescalegis://%2FUsers%2Fpostgres%2FRuN/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgis"
        assert url["HOST"] == "/Users/postgres/RuN"
        assert url["USER"] == ""
        assert url["PASSWORD"] == ""
        assert url["PORT"] == ""

    def test_timescalegis_ipv6_parsing(self) -> None:
        url = dj_database_url.parse(
            "timescalegis://ieRaekei9wilaim7:wegauwhgeuioweg@[2001:db8:1234::1234:5678:90af]:5431/d8r82722r2kuvn"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgis"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "2001:db8:1234::1234:5678:90af"
        assert url["USER"] == "ieRaekei9wilaim7"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431

    def test_timescalegis_search_path_parsing(self) -> None:
        url = dj_database_url.parse(
            "timescalegis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?currentSchema=otherschema"
        )
        assert url["ENGINE"] == "timescale.db.backends.postgis"
        assert url["NAME"] == "d8r82722r2kuvn"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "uf07k1i6d8ia0v"
        assert url["PASSWORD"] == "wegauwhgeuioweg"
        assert url["PORT"] == 5431
        assert url["OPTIONS"]["options"] == "-c search_path=otherschema"
        assert "currentSchema" not in url["OPTIONS"]

    def test_timescalegis_parsing_with_special_characters(self) -> None:
        url = dj_database_url.parse(
            "timescalegis://%23user:%23password@ec2-107-21-253-135.compute-1.amazonaws.com:5431/%23database"
        )

        assert url["ENGINE"] == "timescale.db.backends.postgis"
        assert url["NAME"] == "#database"
        assert url["HOST"] == "ec2-107-21-253-135.compute-1.amazonaws.com"
        assert url["USER"] == "#user"
        assert url["PASSWORD"] == "#password"
        assert url["PORT"] == 5431

    def test_persistent_connection_variables(self) -> None:
        url = dj_database_url.parse(
            "sqlite://myfile.db", conn_max_age=600, conn_health_checks=True
        )

        assert url["CONN_MAX_AGE"] == 600
        assert url["CONN_HEALTH_CHECKS"] is True

    def test_sqlite_memory_persistent_connection_variables(self) -> None:
        # memory sqlite ignores connection.close(), so persistent connection
        # variables aren’t required
        url = dj_database_url.parse(
            "sqlite://:memory:", conn_max_age=600, conn_health_checks=True
        )

        assert "CONN_MAX_AGE" not in url
        assert "CONN_HEALTH_CHECKS" not in url

    @mock.patch.dict(
        os.environ,
        {"DATABASE_URL": "postgres://user:password@instance.amazonaws.com:5431/d8r8?"},
    )
    def test_persistent_connection_variables_config(self) -> None:
        url = dj_database_url.config(conn_max_age=600, conn_health_checks=True)

        assert url["CONN_MAX_AGE"] == 600
        assert url["CONN_HEALTH_CHECKS"] is True

    def test_no_env_variable(self) -> None:
        with self.assertLogs() as cm:
            with mock.patch.dict(os.environ, clear=True):
                url = dj_database_url.config()
            assert url == {}, url
        assert cm.output == [
            'WARNING:root:No DATABASE_URL environment variable set, and so no databases setup'
        ], cm.output

    def test_credentials_unquoted__raise_value_error(self) -> None:
        expected_message = (
            "This string is not a valid url, possibly because some of its parts "
            r"is not properly urllib.parse.quote()'ed."
        )
        with self.assertRaisesRegex(ValueError, re.escape(expected_message)):
            dj_database_url.parse("postgres://user:passw#ord!@localhost/foobar")

    def test_credentials_quoted__ok(self) -> None:
        url = "postgres://user%40domain:p%23ssword!@localhost/foobar"
        config = dj_database_url.parse(url)
        assert config["USER"] == "user@domain"
        assert config["PASSWORD"] == "p#ssword!"

    def test_unknown_scheme__raise_value_error(self) -> None:
        expected_message = (
            "Scheme 'unknown-scheme://' is unknown. "
            "Did you forget to register custom backend? Following schemes have registered backends:"
        )
        with self.assertRaisesRegex(ValueError, re.escape(expected_message)):
            dj_database_url.parse("unknown-scheme://user:password@localhost/foobar")

    def test_register_multiple_times__no_duplicates_in_uses_netloc(self) -> None:
        # make sure that when register() function is misused,
        # it won't pollute urllib.parse.uses_netloc list with duplicates.
        # Otherwise, it might cause performance issue if some code assumes that
        # that list is short and performs linear search on it.
        dj_database_url.register("django.contrib.db.backends.bag_end", "bag-end")
        dj_database_url.register("django.contrib.db.backends.bag_end", "bag-end")
        assert len(uses_netloc) == len(set(uses_netloc))

    @mock.patch.dict(
        os.environ,
        {"DATABASE_URL": "postgres://user:password@instance.amazonaws.com:5431/d8r8?"},
    )
    def test_ssl_require(self) -> None:
        url = dj_database_url.config(ssl_require=True)
        assert url["OPTIONS"] == {'sslmode': 'require'}

    def test_options_int_values(self) -> None:
        """Ensure that options with integer values are parsed correctly."""
        url = dj_database_url.parse(
            "mysql://user:pw@127.0.0.1:15036/db?connect_timout=3"
        )
        assert url["OPTIONS"] == {'connect_timout': 3}

    @mock.patch.dict(
        os.environ,
        {"DATABASE_URL": "postgres://user:password@instance.amazonaws.com:5431/d8r8?"},
    )
    def test_server_side_cursors__config(self) -> None:
        url = dj_database_url.config(disable_server_side_cursors=True)

        assert url["DISABLE_SERVER_SIDE_CURSORS"] is True


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import unittest

import dj_database_url


POSTGIS_URL = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'


class DatabaseTestSuite(unittest.TestCase):

    def test_postgres_parsing(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_postgres_unix_socket_parsing(self):
        url = 'postgres://%2Fvar%2Frun%2Fpostgresql/d8r82722r2kuvn'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == '/var/run/postgresql'
        assert url['USER'] == ''
        assert url['PASSWORD'] == ''
        assert url['PORT'] == ''

    def test_postgres_search_path_parsing(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?currentSchema=otherschema'
        url = dj_database_url.parse(url)
        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431
        assert url['OPTIONS']['options'] == '-c search_path=otherschema'


    def test_postgres_parsing_with_special_characters(self):
        url = 'postgres://%23user:%23password@ec2-107-21-253-135.compute-1.amazonaws.com:5431/%23database'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == '#database'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == '#user'
        assert url['PASSWORD'] == '#password'
        assert url['PORT'] == 5431

    def test_postgis_parsing(self):
        url = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.contrib.gis.db.backends.postgis'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_mysql_gis_parsing(self):
        url = 'mysqlgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.contrib.gis.db.backends.mysql'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_mysql_connector_parsing(self):
        url = 'mysql-connector://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'mysql.connector.django'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_cleardb_parsing(self):
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.mysql'
        assert url['NAME'] == 'heroku_97681db3eff7580'
        assert url['HOST'] == 'us-cdbr-east.cleardb.com'
        assert url['USER'] == 'bea6eb025ca0d8'
        assert url['PASSWORD'] == '69772142'
        assert url['PORT'] == ''

    def test_database_url(self):
        del os.environ['DATABASE_URL']
        a = dj_database_url.config()
        assert not a

        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'

        url = dj_database_url.config()

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_empty_sqlite_url(self):
        url = 'sqlite://'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.sqlite3'
        assert url['NAME'] == ':memory:'

    def test_memory_sqlite_url(self):
        url = 'sqlite://:memory:'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.sqlite3'
        assert url['NAME'] == ':memory:'

    def test_parse_engine_setting(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_database_url.parse(url, engine)

        assert url['ENGINE'] == engine

    def test_config_engine_setting(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        os.environ['DATABASE_URL'] = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_database_url.config(engine=engine)

        assert url['ENGINE'] == engine

    def test_parse_conn_max_age_setting(self):
        conn_max_age = 600
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_database_url.parse(url, conn_max_age=conn_max_age)

        assert url['CONN_MAX_AGE'] == conn_max_age

    def test_config_conn_max_age_setting(self):
        conn_max_age = 600
        os.environ['DATABASE_URL'] = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_database_url.config(conn_max_age=conn_max_age)

        assert url['CONN_MAX_AGE'] == conn_max_age

    def test_database_url_with_options(self):
        # Test full options
        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?sslrootcert=rds-combined-ca-bundle.pem&sslmode=verify-full'
        url = dj_database_url.config()

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431
        assert url['OPTIONS'] == {
            'sslrootcert': 'rds-combined-ca-bundle.pem',
            'sslmode': 'verify-full'
        }

        # Test empty options
        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?'
        url = dj_database_url.config()
        assert 'OPTIONS' not in url

    def test_mysql_database_url_with_sslca_options(self):
        os.environ['DATABASE_URL'] = 'mysql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:3306/d8r82722r2kuvn?ssl-ca=rds-combined-ca-bundle.pem'
        url = dj_database_url.config()

        assert url['ENGINE'] == 'django.db.backends.mysql'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 3306
        assert url['OPTIONS'] == {
            'ssl': {
                    'ca': 'rds-combined-ca-bundle.pem'
            }
        }

        # Test empty options
        os.environ['DATABASE_URL'] = 'mysql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:3306/d8r82722r2kuvn?'
        url = dj_database_url.config()
        assert 'OPTIONS' not in url

    def test_oracle_parsing(self):
        url = 'oracle://scott:tiger@oraclehost:1521/hr'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.oracle'
        assert url['NAME'] == 'hr'
        assert url['HOST'] == 'oraclehost'
        assert url['USER'] == 'scott'
        assert url['PASSWORD'] == 'tiger'
        assert url['PORT'] == 1521

    def test_oracle_gis_parsing(self):
        url = 'oraclegis://scott:tiger@oraclehost:1521/hr'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.contrib.gis.db.backends.oracle'
        assert url['NAME'] == 'hr'
        assert url['HOST'] == 'oraclehost'
        assert url['USER'] == 'scott'
        assert url['PASSWORD'] == 'tiger'
        assert url['PORT'] == 1521

    def test_oracle_dsn_parsing(self):
        url = (
            'oracle://scott:tiger@/'
            '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)'
            '(HOST=oraclehost)(PORT=1521)))'
            '(CONNECT_DATA=(SID=hr)))'
        )
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.oracle'
        assert url['USER'] == 'scott'
        assert url['PASSWORD'] == 'tiger'
        assert url['HOST'] == ''
        assert url['PORT'] == ''

        dsn = (
            '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)'
            '(HOST=oraclehost)(PORT=1521)))'
            '(CONNECT_DATA=(SID=hr)))'
        )

        assert url['NAME'] == dsn

    def test_oracle_tns_parsing(self):
        url = 'oracle://scott:tiger@/tnsname'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.oracle'
        assert url['USER'] == 'scott'
        assert url['PASSWORD'] == 'tiger'
        assert url['NAME'] == 'tnsname'
        assert url['HOST'] == ''
        assert url['PORT'] == ''


if __name__ == '__main__':
    unittest.main()

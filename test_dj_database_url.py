# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import unittest

import dj_database_url
import pdb


POSTGIS_URL = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'


class DatabaseTestSuite(unittest.TestCase):

    def test_truth(self):
        assert True

    def test_postgres_parsing(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
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

    def test_cleardb_parsing(self):
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.mysql'
        assert url['NAME'] == 'heroku_97681db3eff7580'
        assert url['HOST'] == 'us-cdbr-east.cleardb.com'
        assert url['USER'] == 'bea6eb025ca0d8'
        assert url['PASSWORD'] == '69772142'
        assert url['PORT'] is None

    def test_database_url(self):
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

    def test_url_parameters(self):
        url = 'mysql://uf07k1i6d8ia0v:secret@example.com:5431/thdbname?ssl.ca=/etc/certs/mysql-ssl.ca\
&ssl.cert=/etc/certs/mysql-ssl.cert&autocommit=True'
        url = dj_database_url.parse(url)

        assert url['ENGINE'] == 'django.db.backends.mysql'
        assert url['NAME'] == 'thdbname'
        assert url['HOST'] == 'example.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'secret'
        assert url['PORT'] == 5431
        assert url['OPTIONS'] == {
            'ssl' : {
                'ca' : '/etc/certs/mysql-ssl.ca',
                'cert' : '/etc/certs/mysql-ssl.cert'
            },
            'autocommit' : True
        }



if __name__ == '__main__':
    unittest.main()
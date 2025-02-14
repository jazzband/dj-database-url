# CHANGELOG

## Unreleased

* Drop dependency on `typing_extensions`.
* Add Django 5.2 support.

## v2.3.0 (2024-10-23)
* Remove Python 3.8 support.
* Remove Django 3 support.
* Add python 3.13 support.
* Add Django 5.1 to the testing library.

## v2.2.0 (2024-05-28)
* Add disable_server_side_cursors parameter
* Enhance Query String Parsing for Server-Side Binding in Django 4.2 with psycopg 3.1.8+
* Update django 5.0 python compatability by @mattseymour in #239
* Improved internals
* Improved documentation

## v2.1.0 (2023-08-15)

* Add value to int parsing when deconstructing url string.

## v2.0.0 (2023-04-27)

* Update project setup such that we now install as a package.

_Notes_: while this does not alter the underlying application code, we are bumping to
2.0 incase there are unforeseen knock on use-case issues.

## v1.3.0 (2023-03-27)

* Cosmetic changes to the generation of schemes.
* Bump isort version - 5.11.5.
* raise warning message if database_url is not set.
* CONN_MAX_AGE fix type - Optional[int].

## v1.2.0 (2022-12-13)

* Add the ability to add test databases.
* Improve url parsing and encoding.
* Fix missing parameter conn_health_check in check function.

## v1.1.0 (2022-12-12)

* Option for connection health checks parameter.
* Update supported version python 3.11.
* Code changes, various improvments.
* Add project links to setup.py

## v1.0.0 (2022-06-18)

Initial release of code now dj-database-urls is part of jazzband.

* Add support for cockroachdb.
* Add support for the offical MSSQL connector.
* Update License to be compatible with Jazzband.
* Remove support for Python < 3.5 including Python 2.7
* Update source code to Black format.
* Update CI using pre-commit

## v0.5.0 (2018-03-01)

- Use str port for mssql
- Added license
- Add mssql to readme
- Add mssql support using pyodbc
- Fix RST schemas
- Django expects Oracle Ports as strings
- Fix IPv6 address parsing
- Add testing for Python 3.6
- Revert "Add setup.cfg for wheel support"
- added option of postgis backend to also add path parsing. (test added also)
- Support schema definition for redshift
- add redshift support
- Add testing for Python 3.5
- Drop testing for Python 2.6
- Fixes issue with unix file paths being turned to lower case
- add Redis support
- Added SpatiaLite in README.rst

## v0.4.1 (2016-04-06)

- Enable CA providing for MySQL URIs
- Update Readme
- Update trove classifiers
- Updated setup.py description

## v0.4.0 (2016-02-04)

- Update readme
- Fix for python3
- Handle search path config in connect url for postgres
- Add tox config to ease testing against multiple Python versions
- Simplified the querystring parse logic
- Cleaned up querystring parsing
- supports database options
- Added tests for CONN_MAX_AGE
- Added documentation for conn_max_age
- Add in optional support for CONN_MAX_AGE
- Support special characters in user, password and name fields
- Add oracle support
- Added support for percent-encoded postgres paths
- Fixed test_cleardb_parsing test
- Enable automated testing with Python 3.4
- Add URL schema examples to README
- Added support for python mysql-connector

## v0.3.0 (2014-03-10)

- Add .gitignore file
- Remove .pyc file
- Remove travis-ci unsupported python version Per docs http://docs.travis-ci.com/user/languages/python/ "Travis CI support Python versions 2.6, 2.7, 3.2 and 3.3"
- Fix cleardb test
- Add setup.cfg for wheel support
- Add trove classifiers for python versions
- Replace Python 3.1 with Python 3.3
- Add MySQL (GIS) support
- Ability to set different engine

## v0.2.2 (2013-07-17)

- Added spatialite to uses_netloc too
- Added spatialite backend
- Replacing tab with spaces
- Handling special case of sqlite://:memory:
- Empty sqlite path will now use a :memory: database
- Fixing test to actually use the result of the parse
- Adding in tests to ensure sqlite in-memory databases work
- Fixed too-short title underline
- Added :target: attribute to Travis status image in README
- Added docs for default argument to config
- Add "pgsql" as a PostgreSQL URL scheme.
- Add support for blank fields (Django expects '' not None)
- fixed url

## v0.2.1 (2012-06-19)

- Add python3 support
- Adding travis status and tests
- Adding test environment variables
- Adding test for cleardb
- Remove query strings from name
- Adding postgres tests
- Adding tests
- refactor scheme lookup
- RedHat's OpenShift platform uses the 'postgresql' scheme
- Registered postgis URL scheme
- Added `postgis://` url scheme
- Use get() on os.environ instead of an if

## v0.2.0 (2012-05-30)

- Fix parse(s)

## v0.1.4 (2012-05-30)

- Add defaults for env
- Set the DATABASES dict rather than assigning to it

## v0.1.3 (2012-05-01)

- Add note to README on supported databases
- Add support for SQLite
- Clean dependencies

## v0.1.2 (2012-04-30)

- Update readme
- Refactor config and use new parse function

## v0.1.1 (2012-04-30) First release

🐍 ✨

# CHANGELOG

## v0.6.0 (unreleased)

- Add Python 3.9 and Django 3.1 trove classifiers and testing
- Add Django as an explicit dependency
- Add Python 3.8 / Django 3.0 trove classifiers
- Point the ci badge at GH actions
- Moving to github ci
- Set long_description to README.rst
- Update LICENSE to reflect multiple contributors
- Update the build image
- Remove outdated sponsorship link
- Update PostgreSQL Django Backend name
- Add testing for Python 3.7
- Add testing for Django 2.2
- Drop testing for Django < 1.11
- Add Django trove classifiers
- Add testing for Django 2.1
- Add EXPECTED_POSTGRES_ENGINE
- Fix #96 deprecated postgres backend strings

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

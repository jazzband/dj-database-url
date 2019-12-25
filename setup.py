# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst') as readme_rst:
    readme = readme_rst.read()

setup(
    name="dj-database-url",
    version="0.5.0",
    url="https://github.com/jacobian/dj-database-url",
    license="BSD",
    author="Kenneth Reitz",
    author_email="me@kennethreitz.com",
    description="Use Database URLs in your Django Application.",
    long_description=readme,
    py_modules=["dj_database_url"],
    install_requires=["Django>1.11"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)

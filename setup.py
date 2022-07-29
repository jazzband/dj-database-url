# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.rst") as readme_rst:
    readme = readme_rst.read()

setup(
    name="dj-database-url",
    version="1.0.0",
    url="https://github.com/jazzband/dj-database-url",
    license="BSD",
    author="Original Author: Kenneth Reitz, Maintained by: JazzBand Community",
    description="Use Database URLs in your Django Application.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    py_modules=["dj_database_url"],
    install_requires=["Django>3.2"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

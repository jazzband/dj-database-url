from pathlib import Path

from setuptools import setup

readme = Path("README.rst").read_text()

setup(
    name="dj-database-url",
    version="2.1.0",
    url="https://github.com/jazzband/dj-database-url",
    license="BSD",
    author="Original Author: Kenneth Reitz, Maintained by: JazzBand Community",
    description="Use Database URLs in your Django Application.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    packages=["dj_database_url"],
    install_requires=["Django>=3.2", "typing_extensions >= 3.10.0.0"],
    include_package_data=True,
    package_data={
        "dj_database_url": ["py.typed"],
    },
    platforms="any",
    project_urls={
        "GitHub": "https://github.com/jazzband/dj-database-url/",
        "Release log": (
            "https://github.com/jazzband/dj-database-url/blob/master/CHANGELOG.md"
        ),
    },
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
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
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as history_file:
    history = history_file.read()

requirements = ["astropy", "pooch"]

setup_requirements = ["pytest-runner"]

test_requirements = [
    "pytest",
]

setup(
    name="planets",
    version="0.6",
    description="Library to provide planetary constants",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="K.-Michael Aye",
    author_email="kmichael.aye@gmail.com",
    url="https://github.com/michaelaye/planets",
    packages=find_packages(include=["planets"]),
    entry_points={"console_scripts": ["planets=planets.cli:main"]},
    package_dir={"planets": "planets"},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords="planets",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

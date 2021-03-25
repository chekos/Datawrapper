#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "requests>=2.0", "ipython>=7.0"]

setup_requirements = ["Click>=7.0", "requests>=2.0", "ipython>=7.0"]

test_requirements = ["Click>=7.0", "requests>=2.0", "ipython>=7.0"]

setup(
    author="Sergio Sanchez",
    author_email="chekos@tacosdedatos.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="A light-weight wrapper for the Datawrapper API.",
    entry_points={"console_scripts": ["datawrapper=datawrapper.cli:main",],},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="datawrapper",
    name="datawrapper",
    packages=find_packages(include=["datawrapper", "datawrapper.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/chekos/datawrapper",
    version="0.4.4",
    zip_safe=False,
)

from setuptools import setup
import os

VERSION = "1.0rc1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datawrapper",
    description="A light-weight python wrapper for the Datawrapper API (v3). ). NNot developed by Datawrapper.de",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Sergio Sanchez",
    url="https://github.com/chekos/datawrapper",
    project_urls={
        "Issues": "https://github.com/chekos/datawrapper/issues",
        "CI": "https://github.com/chekos/datawrapper/actions",
        "Changelog": "https://github.com/chekos/datawrapper/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datawrapper"],
    install_requires=["ipython>=7.22.0","pandas>=1.1.0","httpx>=0.22.0","rich>=11.0.0","typer>=0.4.0"],
    extras_require={"test": ["pytest"], "dev": ["black", "isort", "pytest", "ipykernel"]},
    python_requires=">=3.6",
)

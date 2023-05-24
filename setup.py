import os
import time

from setuptools import setup
from setuptools_scm.version import guess_next_version


def read(file_name):
    """Read in the supplied file name from the root directory.

    Args:
        file_name (str): the name of the file

    Returns: the content of the file
    """
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


def version_scheme(version):
    """Version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    if version.exact:
        return version.format_with("{tag}")
    else:
        _super_value = version.format_next_version(guess_next_version)
        now = int(time.time())
        return _super_value + str(now)


def local_version(version):
    """Local version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    return ""


setup(
    name="datawrapper",
    description="A light-weight python wrapper for the Datawrapper API",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="chekos",
    author_email="chekos@tacosdedatos.com",
    url="https://github.com/chekos/datawrapper",
    project_urls={
        "Maintainer": "https://github.com/chekos/",
        "Source": "https://github.com/chekos/datawrapper",
        "Tracker": "https://github.com/chekos/datawrapper/issues",
    },
    packages=("datawrapper",),
    install_requires=[
        "importlib_metadata",
        "rich",
        "requests",
        "pandas",
        "ipython",
    ],
    setup_requires=["setuptools_scm"],
    use_scm_version={"version_scheme": version_scheme, "local_scheme": local_version},
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

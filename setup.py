import os
from setuptools import find_packages, setup

from killtracker import __version__, APP_NAME, HOMEPAGE_URL


# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=APP_NAME,
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="An app for running killmail trackers with Alliance Auth and Discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=HOMEPAGE_URL,
    author="Erik Kalkoken",
    author_email="kalkoken87@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires="~=3.6",
    install_requires=[
        "django-esi>=2.0.4",
        "allianceauth>=2.8.0",
        "dataclasses>='0.7';python_version<'3.7'",
        "dacite",
        "django-eveuniverse>=0.6.4",
        "redis-simple-mq>=0.4",
        "dhooks-lite>=0.6",
    ],
)

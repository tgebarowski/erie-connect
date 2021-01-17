import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="erie_connect",
    version="0.4.1",
    url="https://github.com/tgebarowski/erie-connect",
    license='MIT',

    author="Tomasz Gebarowski",
    author_email="gebarowski@gmail.com",

    description="Unofficial Erie Connect cloud client to retrieve data from IQsoft 26 water softener",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=['requests>=2.23.0', 'simplejson>=3.17.0'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

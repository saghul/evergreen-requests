# -*- coding: utf-8 -*-

import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    return re.search(r"""__version__\s+=\s+(?P<quote>['"])(?P<version>.+?)(?P=quote)""", open('evergreen_requests.py').read()).group('version')


setup(
    name                 = 'evergreen-requests',
    version              = get_version(),
    url                  = 'https://github.com/saghul/evergreen-requests',
    license              = 'BSD',
    author               = 'Saúl Ibarra Corretgé',
    author_email         = 'saghul@gmail.com',
    description          = 'Helper module to use requests with evergreen',
    long_description     = open('README.rst', 'r').read(),
    install_requires     = ['evergreen', 'requests'],
    py_modules           = ['evergreen_requests'],
    zip_safe             = False,
    include_package_data = True,
    platforms            = 'any',
    classifiers          = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)


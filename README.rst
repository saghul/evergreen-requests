evergreen-requests
==================

This module contains an asynchronous replica of the ``requests`` API to be used together
with evergreen, allowing you to make asynchronous HTTP requests easily.

All API methods return a ``Request`` instance (as opposed to ``Response``). A list of
requests can be sent with ``map()``.

This is a port to of Kenneth Reitz's grequests (https://github.com/kennethreitz/grequests) module.

Usage
-----

Usage is simple::

    from evergreen.ext import requests

    urls = [
        'http://www.heroku.com',
        'http://tablib.org',
        'http://httpbin.org',
        'http://python-requests.org',
        'http://kennethreitz.com'
    ]

Create a set of unsent Requests::

    >>> rs = (requests.get(u) for u in urls)

Send them all at the same time::

    >>> list(requests.imap(rs))
    [<Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>]


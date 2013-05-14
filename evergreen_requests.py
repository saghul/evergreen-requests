
from functools import partial
from operator import methodcaller

from evergreen import patcher
from evergreen.futures import TaskPoolExecutor

# Monkey-patch.
requests = patcher.import_patched('requests')

__version__ = '0.0.1'

__all__ = ['map', 'get', 'options', 'head', 'post', 'put', 'patch', 'delete', 'request', '__version__']

# Export same items as vanilla requests
__requests_imports__ = ['utils', 'session', 'Session', 'codes', 'RequestException', 'Timeout', 'URLRequired', 'TooManyRedirects', 'HTTPError', 'ConnectionError']
patcher.slurp_properties(requests, globals(), srckeys=__requests_imports__)
__all__.extend(__requests_imports__)
del requests, patcher, __requests_imports__


class AsyncRequest(object):
    """ Asynchronous request.

    Accept same parameters as ``Session.request`` and some additional:

    :param session: Session which will do the request, else one is created automatically.
    :param callback: Callback called on response. Same as passing ``hooks={'response': callback}``.
    """
    def __init__(self, method, url, **kwargs):
        self.method = method
        self.url = url
        self.session = kwargs.pop('session', None)
        if self.session is None:
            self.session = Session()
        callback = kwargs.pop('callback', None)
        if callback:
            kwargs['hooks'] = {'response': callback}
        self.kwargs = kwargs  # Arguments for ``Session.request``
        self.response = None

    def send(self, **kwargs):
        """
        Prepares request based on parameter passed to constructor and optional ``kwargs```.
        Then sends request and saves response to :attr:`response`

        :returns: ``Response``
        """
        merged_kwargs = {}
        merged_kwargs.update(self.kwargs)
        merged_kwargs.update(kwargs)
        self.response = self.session.request(self.method, self.url, **merged_kwargs)
        return self.response


# Shortcuts for creating AsyncRequest with appropriate HTTP method
get = partial(AsyncRequest, 'GET')
options = partial(AsyncRequest, 'OPTIONS')
head = partial(AsyncRequest, 'HEAD')
post = partial(AsyncRequest, 'POST')
put = partial(AsyncRequest, 'PUT')
patch = partial(AsyncRequest, 'PATCH')
delete = partial(AsyncRequest, 'DELETE')

def request(method, url, **kwargs):
    return AsyncRequest(method, url, **kwargs)


def map(reqs, concurrency=10):
    """Concurrently converts a list of Requests to Responses.

    :param reqs: a collection of AsyncRequest objects.
    :param concurrency: Specifies the number of requests to make at a time. Defaults to 10.
    """

    def result_iterator():
        with TaskPoolExecutor(concurrency) as executor:
            for r in executor.map(methodcaller('send'), list(reqs)):
                yield r
    return result_iterator()


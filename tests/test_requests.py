
# Path hack
import os, sys
sys.path.insert(0, os.path.abspath('..'))

import time
import unittest

from evergreen.ext import requests


HTTPBIN_URL = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')

def httpbin(*suffix):
    """Returns url for HTTPBIN resource."""
    return HTTPBIN_URL + '/'.join(suffix)


N = 5
URLS = [httpbin('get?p=%s' % i) for i in range(N)]


class RequestsTest(unittest.TestCase):

    def test_map(self):
        reqs = [requests.get(url) for url in URLS]
        resp = requests.map(reqs, concurrency=N)
        self.assertEqual([r.url for r in resp], URLS)

    def test_hooks(self):
        result = {}

        def hook(r, **kwargs):
            result[r.url] = True

        hooks = dict(response=[hook])
        reqs = [requests.get(url, hooks=hooks) for url in URLS]
        resp = list(requests.map(reqs, concurrency=N))
        self.assertEqual(sorted(result.keys()), sorted(URLS))

    def test_callback_kwarg(self):
        result = {'ok': False}

        def callback(r, **kwargs):
            result['ok'] = True

        self.get(URLS[0], callback=callback)
        self.assertTrue(result['ok'])

    def test_session_and_cookies(self):
        c1 = {'k1': 'v1'}
        r = self.get(httpbin('cookies/set'), params=c1).json()
        self.assertEqual(r['cookies'], c1)
        s = requests.Session()
        r = self.get(httpbin('cookies/set'), session=s, params=c1).json()
        self.assertEqual(dict(s.cookies), c1)

        # ensure all cookies saved
        c2 = {'k2': 'v2'}
        c1.update(c2)
        r = self.get(httpbin('cookies/set'), session=s, params=c2).json()
        self.assertEqual(dict(s.cookies), c1)

        # ensure new session is created
        r = self.get(httpbin('cookies')).json()
        self.assertEqual(r['cookies'], {})

        # cookies as param
        c3 = {'p1': '42'}
        r = self.get(httpbin('cookies'), cookies=c3).json()
        self.assertEqual(r['cookies'], c3)

    def test_calling_request(self):
        reqs = [requests.request('POST', httpbin('post'), data={'p': i})
                for i in range(N)]
        resp = requests.map(reqs, concurrency=N)
        self.assertEqual([int(r.json()['form']['p']) for r in resp], list(range(N)))

    def test_stream_enabled(self):
        r = list(requests.map([requests.get(httpbin('stream/10'), stream=True)], concurrency=2))[0]
        self.assertFalse(r._content_consumed)

    def test_concurrency_with_delayed_url(self):
        t = time.time()
        n = 10
        reqs = [requests.get(httpbin('delay/1')) for _ in range(n)]
        resp = list(requests.map(reqs, concurrency=n))
        self.assertLess((time.time() - t), n)

    def get(self, url, **kwargs):
        return list(requests.map([requests.get(url, **kwargs)]))[0]


if __name__ == '__main__':
    unittest.main(verbosity=2)


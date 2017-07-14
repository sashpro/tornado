import main
from tornado.testing import AsyncTestCase, gen_test
from tornado import gen, httpclient
from settings import PORT
import json


class TestApp(AsyncTestCase):
    request_timeout=1000
    connection_cnt = 1000
    urls = [
        'http://google.com',
    ]
    expected_response = {
        "links": [
            {
                "url": "http://google.com",
                "title": "Google"
            }
        ]
    }
    def setUp(self):
        super().setUp()
        self.app_address = 'http://localhost:{}'.format(PORT)
        self.request_payload = ' '.join(self.urls)


    @gen_test(timeout=request_timeout)
    def test_analyze(self):
        self.client = httpclient.AsyncHTTPClient(self.io_loop)
        request = httpclient.HTTPRequest(self.app_address + '/analyze', method='POST', headers=None, body=self.request_payload,
             request_timeout=self.request_timeout, connect_timeout=self.request_timeout)

        response_fut = [self.client.fetch(request) for _ in range(self.connection_cnt)]
        response = yield response_fut
        for resp in response:
            self.assertEqual(json.loads(resp.body.decode()), self.expected_response)

        # self.assertEqual(response.body, b'Hello, world')    
    # def test_homepage(self):
    #     response = self.fetch('/')
    #     self.assertEqual(response.code, 200)
    #     self.assertEqual(response.body, 'Hello, world')

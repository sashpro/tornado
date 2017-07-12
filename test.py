import main
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado import gen, httpclient
import random
import urllib
import time 


class TestApp(AsyncHTTPTestCase):
    def get_app(self):
        return main.make_app()

    # @gen_test
    def test_home(self):
        response = self.fetch('/')
        # response = yield gen.Task(self.fetch('/'))
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'Hello, world')    

    # @gen_test
    # def test_analyze(self):
    #     for it in (self.get_data() for i in range(1000)):

    #         it.next()

    @gen_test(timeout=5)
    def test_analyze(self):
        # post_data = { 'url': 'http://www.google.com;'}
        post_data = { 'url': 'http://127.0.0.1:3000 https://codeguida.com http://127.0.0.1:3000'} 
        body = urllib.parse.urlencode(post_data)
        # response = yield self.http_client.fetch(self.get_url('/analyze'), method='POST', headers=None, body=body)
        tasks = ['k%s'%i for i in range(11)]
        # print(list(tasks))
        # http_client = httpclient.AsyncHTTPClient()
        urls = ['http://google.com', 'http://gmail.com', 'http://codeguida.com', 'http://twitter.com','http://linkedin.com']
        
        for task in tasks:
            url = random.choice(urls)
            body = urllib.parse.urlencode({'url':url})
            # print(time.time(), url)
            self.http_client.fetch(self.get_url('/analyze'), method='POST', headers=None, body=body,
                 callback=(yield gen.Callback(task)))
        response = yield gen.WaitAll(list(tasks))

        # print(response)
        for resp in response:
            print(resp.body)
            self.assertEqual(resp.code, 200)

        # self.assertEqual(response.body, b'Hello, world')    
    # def test_homepage(self):
    #     response = self.fetch('/')
    #     self.assertEqual(response.code, 200)
    #     self.assertEqual(response.body, 'Hello, world')

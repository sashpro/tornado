# encoding -*-: utf-8
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import asynchronous
from bs4 import BeautifulSoup
from settings import PORT
import time
import re
import json


class AnalyzeHandler(tornado.web.RequestHandler):
    request_timeout = 60
    @gen.coroutine

    def post(self):        
        content = self.request.body.decode() 
        comp = re.compile(r'https?://[^\s]+') 
        urls = comp.findall(content)
        http_client = AsyncHTTPClient()
        response_futures = [
            http_client.fetch(HTTPRequest(url, request_timeout=self.request_timeout)) for url in urls]
        responses = yield response_futures
        links=[]
        for url, response in zip(urls, responses):
            body_data = response.body
            soup = BeautifulSoup(body_data, 'html.parser')
            links.append(
                {
                    'url': url,
                    'title': soup.find('title').contents[0],
                }
            )
        response = {'links': links}
        self.write(json.dumps(response))


class MainHandler(tornado.web.RequestHandler):
    # @gen.coroutine        
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/analyze", AnalyzeHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    tornado.ioloop.IOLoop.instance().start()

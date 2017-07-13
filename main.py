# encoding -*-: utf-8
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import asynchronous
from bs4 import BeautifulSoup
import time
import re


class AnalyzeHandler(tornado.web.RequestHandler):
    @gen.coroutine
    # @gen.engine    
    # @shortgen    
    def post(self):
        
        links = {'links':[]}  
        url=''.join(self.get_arguments('url'))
        comp = re.compile(r'https?://[^\s]+') 
        adr = comp.findall(url)

        print(url)

        link = a[0]
        start = time.time()
        http_client = AsyncHTTPClient()
        response_futures = [
            http_client.fetch(HTTPRequest(url, request_timeout=self.request_timeout)) for url in adr]
        responses = yield response_futures
            #resp = yield http_client.fetch(link)
            # resp = await gen.Task(http_client.fetch, link)
            #print(time.time()-start, link)
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
    # @asynchronous
    # def post(self):
    #     self.write("post hello")
        # time.sleep(200)

    # @gen.coroutine        
    def get(self):
        self.write("Hello, world")
    #     fut = yield self.fin() 

    # @gen.coroutine
    # def fin(self):
    #     time.sleep(3)
    #     self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/analyze", AnalyzeHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    tornado.ioloop.IOLoop.instance().start()

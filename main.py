# encoding -*-: utf-8
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.web import asynchronous
from bs4 import BeautifulSoup
import time
import re


class AnalyzeHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    # @gen.engine    
    # @shortgen    
    def post(self):
        
        links = {'links':[]}  
        url=''.join(self.get_arguments('url'))
        comp = re.compile(r'(((http|https):\/\/)?(w{3}\.)?(\w+\.?)+(:\d{4})?)') 
        adr = comp.findall(url)
        for a in adr:
            print(url)

            link = a[0]
            start = time.time()
            http_client = AsyncHTTPClient()
            resp = yield http_client.fetch(link)
            # resp = await gen.Task(http_client.fetch, link)
            print(time.time()-start, link)
            soup = BeautifulSoup(resp.body,"html.parser")
            links['links'].append({
                   "url": link,
                   "title": soup.find('title').getText()
                })
        # data = yield self.analyze()
        # print(links)    
        self.write(links)
        self.finish()


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
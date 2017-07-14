import tornado.ioloop

from tornado.httpserver import HTTPServer

from invoke import task
from main import  make_app

from settings import PORT


@task
def run_dev(ctx):
    server = HTTPServer(make_app())
    server.bind(PORT)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
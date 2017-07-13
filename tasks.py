import tornado.ioloop

from tornado.httpserver import HTTPServer

from invoke import task
from highchat.app import app

from settings import PORT


@task
def run_dev(ctx):
    server = HTTPServer(app)
    server.bind(PORT)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
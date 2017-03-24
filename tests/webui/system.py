#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Dealer
from .simplemod import SimpleModule
from entropyfw.common.request import Request

__author__ = 'otger'


class WebUISystem(object):

    def __init__(self, flask_app):
        self.dealer = Dealer()
        self.m1 = SimpleModule(name='adder', dealer=self.dealer, flask_app=flask_app)

    def exit(self):
        self.dealer.exit()

    def sum(self, a, b):
        r = Request(command_id=0,
                    source='myself',
                    target='adder',
                    command='addition',
                    arguments={'s1': a, 's2': b})
        self.dealer.request(r)
        # r.wait_answer()
        # print(r.return_value)
        return r

    def list_functionality(self):
        r = Request(command_id=0,
                    source='myself',
                    target='adder',
                    command='listregisteredactions')
        self.dealer.request(r)
        r.wait_answer()
        s = "Functionality of module 'adder': \n"
        for el in r.return_value:
            s += "\t - {0}\n".format(', '.join([str(x) for x in el]))
        print(s)
        return r

if __name__ == "__main__":
    from entropyfw.logger import log, formatter
    import logging

    from gevent.wsgi import WSGIServer
    from flask import Flask, url_for
    app = Flask(__name__)
    server = WSGIServer(("", 5000), app)
    server.start()


    def list_routes():
        import urllib
        output = []
        for rule in app.url_map.iter_rules():

            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)

        for line in sorted(output):
            print(line)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    s = WebUISystem(flask_app=app)
    print(app.url_map)

    log.info('Created system')
    r = s.sum(1, 2)
    log.info('Asked int sum')
    log.info("Sum(1,2) returned: {0}".format(r.return_value))
    r.wait_answer()
    r = s.sum('a', 'b')
    log.info('Asked str sum')
    r.wait_answer()
    log.info("Sum('a', 'b') returned: {0}".format(r.return_value))
    s.list_functionality()

    s.exit()
    # list_routes()
    server.serve_forever()

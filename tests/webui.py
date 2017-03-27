#!/usr/bin/python
# -*- coding: utf-8 -*-

from webui.system import WebUISystem
"""
webui
Created by otger on 27/03/17.
All rights reserved.
"""

if __name__ == "__main__":
    from entropyfw.logger import log, formatter
    import logging

    from gevent.wsgi import WSGIServer
    from flask import Flask, url_for

    from flask.templating import DispatchingJinjaLoader

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

    def list_templates():
        d = DispatchingJinjaLoader(app)
        print(d.list_templates())

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    s = WebUISystem(flask_app=app)
    print(app.url_map)
    list_templates()
    print(app.blueprints.items())
    print(app.blueprints['sys_bp'].static_folder, app.blueprints['sys_bp'].root_path)
    print(app.blueprints['adder'].static_folder, app.blueprints['adder'].root_path)

    log.info('Created system')
    r = s.sum(1, 2)
    log.info('Asked int sum')
    r.wait_answer()
    log.info("Sum(1,2) returned: {0}".format(r.return_value))
    r = s.sum('a', 'b')
    log.info('Asked str sum')
    r.wait_answer()
    log.info("Sum('a', 'b') returned: {0}".format(r.return_value))
    s.list_functionality()

    s.exit()
    # list_routes()
    server.serve_forever()

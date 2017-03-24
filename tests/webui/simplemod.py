#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Module
from .action import Addition
from .web.blueprints import get_blueprint

__author__ = 'otger'


class SimpleModule(Module):
    name = 'simplemod'

    def __init__(self, dealer, name=None, flask_app=None):
        Module.__init__(self, name=name, dealer=dealer, flask_app=flask_app)
        self.register_action(Addition)

    def init_flask_blueprints(self):
        self.flask_app.register_blueprint(get_blueprint(self.name))





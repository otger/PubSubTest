#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Module
from .action import Addition
from .web.blueprints import get_blueprint
from .api.resources import get_api_resources

__author__ = 'otger'


class SimpleModule(Module):
    name = 'simplemod'

    def __init__(self, name=None):
        Module.__init__(self, name=name)
        self.register_action(Addition)
        self.register_blueprint(get_blueprint(self.name))
        for r in get_api_resources():
            self.register_api_resource(r)

    @staticmethod
    def sum(a, b):
        return a+b





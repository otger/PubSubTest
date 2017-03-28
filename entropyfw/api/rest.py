#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Api, Resource

"""
rest
Created by otger on 29/03/17.
All rights reserved.
"""


class ModuleResource(Resource):

    def __init__(self, module, url, kwargs={}):
        self.mod = module
        self.url = url.lstrip('/')
        self.kwargs = kwargs
        super(ModuleResource, self).__init__()

    def get_url(self):
        return '/api/{0}/{1}'.format(self.mod.name, self.url)


class ApiManager(object):
    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.api = None
        if self.flask_app:
            self.api = Api(self.flask_app)

    def add_resources(self, module):
        for r in module.get_api_resources():
            self.api.add_resource(r, r.get_url(), **r.kwargs)

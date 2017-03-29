#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Api, Resource

"""
rest
Created by otger on 29/03/17.
All rights reserved.
"""


class ModuleResource(Resource):

    url = ''
    description = ''

    def __init__(self, module):
        self.module = module
        super(ModuleResource, self).__init__()


class ApiManager(object):
    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.api = None
        self.resources = {}
        if self.flask_app:
            self.api = Api(self.flask_app)

    @staticmethod
    def get_resource_url(resource, module):
        endpoint = resource.__name__.lower()
        if resource.url:
            endpoint = resource.url
        return '/api/{0}/{1}'.format(module.name, endpoint)

    def add_resources(self, module, resources=[]):
        if not resources:
            resources = module.get_api_resources()
        for r in resources:
            url = self.get_resource_url(r, module)
            self.resources[url] = r
            self.api.add_resource(r, url,
                                  resource_class_kwargs={'module': module})

    def list_resources(self):
        return {k: {'description': v.description} for k, v in self.resources.items()}

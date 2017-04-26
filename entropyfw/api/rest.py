#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restful import Api, Resource, request
from .logger import log
import traceback
from flask import jsonify
from entropyfw.common import get_utc_ts

"""
rest
Created by otger on 29/03/17.
All rights reserved.
"""


class REST_STATUS(object):
    Done = 'Done'  # Command has been executed without problems
    Error = 'Error'  # An exception raised when executing command


class ModuleResource(Resource):

    url = ''
    description = ''

    def __init__(self, module):
        self.module = module
        self._init_ts = get_utc_ts()
        super(ModuleResource, self).__init__()

    def jsonify_return(self, status=REST_STATUS.Done, result=None, **kwargs):
        """
        Jsonify return values of a REST command
        If the command resulted in an error status must be REST_STATUS.Error and message should contain error message
        :param status:
        :param result:
        :param kwargs:
        :return:
        """
        res = {'utc_start': self._init_ts,
               'utc_end': get_utc_ts(),
               'status': status,
               'result': result,
               'url': request.url}

        res.update(kwargs)
        return jsonify(res)


class MyApi(Api):

    def handle_error(self, e):
        code = getattr(e, 'code', 500)
        # log.debug("Error while processing request. {0}".format(traceback.format_exc()))
        log.exception("Error while processing request")
        log.debug('Request headers: {0}'.format(request.headers))
        log.debug('Request data: {0}'.format(request.data))
        return super(MyApi, self).handle_error(e) # for all other errors than 500 use flask-restful's default error handling


class ApiManager(object):
    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.api = None
        self.resources = {}
        if self.flask_app:
            self.api = MyApi(self.flask_app)

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
            self.api.add_resource(r, url, endpoint='{}.{}'.format(module.name, r.url),
                                  resource_class_kwargs={'module': module})

    def list_resources(self):
        return {k: {'description': v.description} for k, v in self.resources.items()}

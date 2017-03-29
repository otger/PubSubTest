#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.api.rest import ModuleResource
from flask import jsonify
from flask_restful import reqparse
"""
resources
Created by otger on 29/03/17.
All rights reserved.
"""


class Sum(ModuleResource):
    url = 'info'

    def __init__(self, module):
        super(Sum, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('arg1', type=, default = "", location = 'json')

    def get(self):

        return jsonify({'args': [a,b],
                        'result': self.module.sum(a, b)})


def get_api_resources():
    return [SysInfo]


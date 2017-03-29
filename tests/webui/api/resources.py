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
    url = 'sum'
    description = 'Adds two arguments, arg1 and arg2'

    def __init__(self, module):
        super(Sum, self).__init__(module)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('arg1', type=float, required=True, location='json')
        self.reqparse.add_argument('arg2', type=float, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        return jsonify({'args': [args['arg1'], args['arg2']],
                        'result': self.module.sum(args['arg1'], args['arg2'])})


def get_api_resources():
    return [Sum]


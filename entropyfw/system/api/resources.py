#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.api.rest import ModuleResource
from flask import jsonify
"""
resources
Created by otger on 29/03/17.
All rights reserved.
"""


class SysInfo(ModuleResource):
    url = 'info'
    description = 'Provide information of the system'

    def __init__(self, module):
        super(SysInfo, self).__init__(module)

    def get(self):

        return jsonify({'modules': {'names': self.module.info.mod_names},
                        'dealer': {'stats': self.module.info.dealer_stats,
                                   'num_players': self.module.info.num_players}
                        })


class ListApi(ModuleResource):
    url = 'list_api'
    description = 'List all defined api endpoints'

    def __init__(self, module):
        super(ListApi, self).__init__(module)

    def get(self):
        return jsonify(self.module.api.list_resources())


def get_api_resources():
    return [SysInfo, ListApi]


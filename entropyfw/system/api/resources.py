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

    def __init__(self, module):
        super(SysInfo, self).__init__(module)

    def get(self):

        return jsonify({'modules': {'names': self.mod.info.mod_names},
                        'dealer': {'stats': self.mod.info.dealer_stats,
                                   'num_players': self.mod.info.num_players}
                        })


def get_api_resources():
    return [SysInfo]


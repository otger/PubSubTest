#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.api.rest import ModuleResource
from flask import jsonify
"""
resources
Created by otger on 29/03/17.
All rights reserved.
"""


class DealerStats(ModuleResource):
    def __init__(self, module):
        super(DealerStats, self).__init__(module, url='dealer_stats', kwargs={})

    def get(self):

        return jsonify({'module_names': self.mod.info.mod_names,
                        'dealer_stats': self.mod.info.dealer_stats,
                        'num_players': self.mod.info.num_players})


def get_api_resources():
    return [DealerStats]


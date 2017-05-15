#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.api.rest import ModuleResource, REST_STATUS
from .logger import log
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
        try:
            values = {'modules': {'names': self.module.info.mod_names},
                      'dealer': {'stats': self.module.info.dealer_stats,
                                 'num_players': self.module.info.num_players}
                      }
        except Exception as ex:
            log.exception('Exception when Acquiring system information')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex))
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=values)


class ListApi(ModuleResource):
    url = 'list_api'
    description = 'List all defined api endpoints'

    def __init__(self, module):
        super(ListApi, self).__init__(module)

    def get(self):
        try:
            values = self.module.api.list_resources()
        except Exception as ex:
            log.exception('Exception when reading api resources')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex))
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=values)


class ListEvents(ModuleResource):
    url = 'list_events'
    description = 'List all events published on a system and number of occurrences'

    def __init__(self, module):
        super(ListEvents, self).__init__(module)

    def get(self):
        try:
            values = {'events': {'names': self.module.info.event_stats}
                      }
        except Exception as ex:
            log.exception('Exception when Acquiring system information')
            return self.jsonify_return(status=REST_STATUS.Error, result=str(ex))
        else:
            return self.jsonify_return(status=REST_STATUS.Done, result=values)


def get_api_resources():
    return [SysInfo, ListApi, ListEvents]


#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.dealer.dealer import Dealer
from entropyfw.common.request import Request
from entropyfw.api.rest import ApiManager

from .web.blueprints import get_blueprints
from .api.resources import get_api_resources

"""
system
Created by otger on 27/03/17.
All rights reserved.
"""


class System(object):
    name = 'system'

    def __init__(self, flask_app=None):
        self.dealer = Dealer()
        self.modules = ModHolder()
        self.info = SystemInfo(system=self)
        self.flask_app = flask_app
        self.api = ApiManager(flask_app=flask_app)
        if flask_app:
            self._register_system_blueprints()
            self._register_sys_api_resources()

    def exit(self):
        self.dealer.exit()

    def add_module(self, module):
        if module.name == self.name:
            raise Exception("Module can't be named '{0}'".format(self.name))
        module.set_dealer(self.dealer)
        module.set_sys_info(self.info)
        self.modules.add_module(module)
        self.register_mod_api(module)
        self.register_blueprints(module)

    def send_request(self, target, command, arguments={}):
        r = Request(command_id=0,
                    source='system',
                    target=target,
                    command=command,
                    arguments=arguments)

        self.dealer.request(r)
        # r.wait_answer()
        # print(r.return_value)
        return r

    def _register_system_blueprints(self):
        """
        Registers system blueprints to flask app
        :return:
        """
        if self.flask_app:
            for bp in get_blueprints():
                bp.set_sys_info(self.info)
                self.flask_app.register_blueprint(bp)

    def _register_sys_api_resources(self):
        self.api.add_resources(self, resources=get_api_resources())

    def register_mod_api(self, module):
        """
        Registers api resources if self.flask_app has been set
        :param module:
        :return:
        """
        if self.flask_app:
            self.api.add_resources(module)

    def register_blueprints(self, module=None):
        """
        If flask_app is set configures blueprints to it. If module is provided, only registers
        blueprints of that module, if module is not set, registers blueprints of all configured modules
        :param module:
        :return:
        """
        if self.flask_app:
            if module:
                for bp in module.get_blueprints():
                    bp.set_sys_info(self.info)
                    self.flask_app.register_blueprint(bp)
            else:
                for m in self.modules:
                    self.register_blueprints(module=m)


class SystemInfo(object):
    def __init__(self, system):
        self.sys = system

    def _get_module_names(self):
        return self.sys.modules.names
    mod_names = property(_get_module_names)

    def _get_module_descriptions(self):
        return self.sys.modules.descriptions
    mod_descriptions = property(_get_module_descriptions)

    def _get_num_players(self):
        return self.sys.dealer.players.num_players
    num_players = property(_get_num_players)

    def _get_dealer_stats(self):
        return self.sys.dealer.stats.get_stats()
    dealer_stats = property(_get_dealer_stats)


class ModHolder(object):
    def __init__(self):
        self.modules = {}
        self._mod_names = []
        self._cache = {'names': None,
                       'descriptions': None}

    def add_module(self, module):
        self._cache['names'] = None
        self._cache['descriptions'] = None
        self.modules[module.name] = module

    def _get_names(self):
        if self._cache['names'] is None:
            self._cache['names'] = self.modules.keys()
        return self._cache['names']
    names = property(_get_names)

    def _get_descriptions(self):
        if self._cache['descriptions'] is None:
            self._cache['descriptions'] = {k: self.modules[k].description for k in self.modules.keys()}
        return self._cache['descriptions']
    descriptions = property(_get_descriptions)

    def __getitem__(self, item, default=None):
        return self.modules.get(item, default)

    def __iter__(self):
        for v in self.modules.items():
            yield v

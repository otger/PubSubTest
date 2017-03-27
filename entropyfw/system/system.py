#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.dealer.dealer import Dealer
from entropyfw.common.request import Request

from .web.blueprints import get_blueprints

"""
system
Created by otger on 27/03/17.
All rights reserved.
"""


class System(object):

    def __init__(self, flask_app=None):
        self.dealer = Dealer()
        self.modules = ModHolder()
        self.info = SystemInfo(system=self)
        self.flask_app = flask_app
        if flask_app:
            self._register_system_blueprints()

    def exit(self):
        self.dealer.exit()

    def add_module(self, module):
        module.set_dealer(self.dealer)
        module.set_sys_info(self.info)
        self.modules.add_module(module)
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

    def register_blueprints(self, module=None, flask_app=None):
        """
        If flask_app is set, sets flask_app and configures blueprints to it. If module is provided, only registers
        blueprints of that module, if module is not set, registers blueprints of all configured modules
        :param module:
        :param flask_app:
        :return:
        """
        if flask_app:
            self.flask_app = flask_app
            self._register_system_blueprints()
        if self.flask_app:
            if module:
                for bp in module.get_blueprints():
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


class ModHolder(object):
    def __init__(self):
        self.modules = {}
        self._mod_names = []

    def add_module(self, module):
        self.modules[module.name] = module

    def _get_names(self):
        return self.modules.keys()
    names = property(_get_names)

    def __getitem__(self, item, default=None):
        return self.modules.get(item, default)

    def __iter__(self):
        for v in self.modules.items():
            yield v

#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue

from .player import Player
from .logger import log
from .worker import Worker
from .actionmanager import ActionManager
from .eventcallbacks import EventCallbacks
from .web import ModuleWebManager

__author__ = 'otger'


class Module(Player):
    name = 'ModuleName'
    description = 'A base class of an entropy system module'

    def __init__(self, name=None):
        Player.__init__(self, name=name)
        self.sys_info = None
        self.actions = ActionManager(self)
        self.cbs = EventCallbacks(self)
        self.web = ModuleWebManager(self)
        self.worker = Worker()
        self.worker.start()

    def set_sys_info(self, sys_info):
        self.sys_info = sys_info
        self.web.set_sys_info(sys_info)

    def get_blueprints(self):
        return self.web.get_blueprints()

    def get_api_resources(self):
        return self.web.get_api_resources()

    def check_event(self, event):
        """Dealer player abstract method
        When dealer receives a new event it distributes it to all players who must check if it has a subscription to it and add to its own queue
        """
        self.cbs.check_event(event)

    def check_request(self, request):
        self.actions.check_request(request)

    def register_callback(self, callback, pattern, flags=0):
        self.cbs.register_callback(callback, pattern, flags)

    def register_action(self, action):
        self.actions.register_action(action)

    def register_blueprint(self, blueprint):
        self.web.register_blueprint(blueprint)

    def register_api_resource(self, resource):
        self.web.register_api_resource(resource)

    def _exit(self):
        """
        Tasks to be performed on closing
        :return:
        """
        self.worker.exit()

    def exit(self):
        """
        Method executed when an exit event is received. If module has to execute something in particular,
        it must overwrite this method
        :return: None
        """
        pass

    def list_callbacks(self):
        return self.cbs.subs.list_subscriptions()
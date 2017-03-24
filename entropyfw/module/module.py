#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue

from .player import Player
from .logger import log
from .worker import Worker
from .actionmanager import ActionManager
from .eventcallbacks import EventCallbacks

__author__ = 'otger'


class Module(Player):
    name = 'ModuleName'

    def __init__(self, dealer, name=None, flask_app=None):
        Player.__init__(self, dealer=dealer, name=name)
        self.actions = ActionManager(self)
        self.cbs = EventCallbacks(self)
        self.worker = Worker()
        self.worker.start()
        self.flask_app = flask_app
        if flask_app:
            self.init_flask_blueprints()

    def init_flask_blueprints(self):
        # Child classes can register flask blueprints if flask_app is a valid value
        pass

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


#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from .logger import log
from .callables import Action
from entropyfw.common.exceptions import CommandNotImplemented
from .internactions import ListRegisteredActions
__author__ = 'otger'


class ActionManager(object):
    def __init__(self, module, limit_history=500):
        self.module = module
        self.actions = {}
        self.history = []
        self.request_errors = []
        self._lim_hist = limit_history

        # Register internal actions
        self.register_action(ListRegisteredActions)

    def register_action(self, action):
        if not issubclass(action, Action):
            raise TypeError("action must be a class which inherits from Action")

        if action.name in self.actions:
            raise KeyError("action already exists")

        self.actions[action.name] = action

    def check_request(self, request):
        # requested_command = request.command
        log.debug('Checking request at module {0}'.format(self.module.name))
        if request.command in self.actions:
            action = self.actions[request.command](request, self, self.module)
            log.debug('Adding action to module {0} worker'.format(self.module.name))
            self.module.worker.put_action(action)
            self.history.append(action)
            if self._lim_hist > 0:
                self.history = self.history[-1*self._lim_hist:]
        else:
            # Command is not implemented
            log.error("'{0}' command is not implemented in module {1} of type {2}".format(request.command, self.module.name, type(self.module)))
            try:
                self.request_error(request)
                ex = CommandNotImplemented("{0} not implemented".format(request.command))
                request.set_error(ex)
            except:
                pass

    def request_error(self, request):
        """To be executed by Actions if it fails to run"""
        self.request_errors.append(request)

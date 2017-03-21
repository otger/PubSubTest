#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import abc
from .logger import log

__author__ = 'otger'


class Action(object):
    __metaclass__ = abc.ABCMeta
    """Base class for all actions to be performed on a module"""
    name = 'action' # To be filled on child class

    def __init__(self, parent, request):
        self._p = parent
        self.request = request
        self.ts = datetime.utcnow().timestamp()
        self.required_arguments = []

    def define_argument(self, name):
        self.required_arguments.append(name)

    def get_arg(self, name):
        return self.request.get_arg(name)

    def run(self):
        try:
            retval = self.functionality()
        except Exception as ex:
            log.error("Error executing Action {0}".format(self.name))
            self.request.set_error(ex)
        else:
            self.request.set_return_value(retval)

    @abc.abstractmethod
    def functionality(self):
        pass


class ActionManager(object):
    def __init__(self):
        self.actions = {}
        self.history = []
        self.errors = []

    def register_action(self, action):
        if not issubclass(action, Action):
            raise TypeError("action must be a class which inherits from Action")

        if action.name in self.actions:
            raise KeyError("action already exists")

        self.actions[action.name] = action

    def check_request(self, request):
        # requested_command = request.command
        return request.command in self.actions


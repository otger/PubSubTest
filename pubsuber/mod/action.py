#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import abc

__author__ = 'otger'


class Action(object):
    __metaclass__ = abc.ABCMeta
    """Base class for all actions to be performed on a module"""

    def __init__(self, parent, name, arguments=[], ):
        self._p = parent
        self.ts = datetime.utcnow().timestamp()

    @abc.abstractmethod
    def run(self, *args, **kwargs):



class Error(object):
    def __init__(self, name, args=[], kwargs={}):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.ts = datetime.utcnow().timestamp()


class ActionManager(object):
    def __init__(self, parent):
        self.parent = parent
        self.actions = {}
        self.history = []
        self.errors = []

    def register_action(self, action):
        if not isinstance(action, Action):
            raise TypeError("action must be of type Action")

        if action.name in self.actions:
            raise KeyError("action already exists")



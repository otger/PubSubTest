#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import abc
from .logger import log

__author__ = 'otger'


class CallableObject(object):
    __metaclass__ = abc.ABCMeta
    """Base class for all callables of a module (callbacks and action)"""
    name = 'callable'  # To be filled on child class

    def __init__(self):
        self.ts = datetime.utcnow().timestamp()

    def run(self):
        try:
            retval = self.functionality()
        except Exception as ex:
            log.exception("Error executing {0}".format(self.name))
            self.set_exception(ex)
        else:
            self.set_return_value(retval)

    @abc.abstractmethod
    def functionality(self):
        pass

    def set_exception(self, ex):
        """Method to be overwritten on child classes if it needs to be notified
        of an exception during execution"""
        pass

    def set_return_value(self, value):
        """Method to be overwritten on child classes if it needs to set return
        value of the execution"""
        pass


class Action(CallableObject):
    __metaclass__ = abc.ABCMeta
    """Base class for all actions to be performed on a module"""
    # To be filled on child class
    name = 'action'
    arguments = []
    description = ""
    version = "0.0"

    def __init__(self, request, manager, module):
        CallableObject.__init__(self)
        self.request = request
        self.am = manager  # action manager
        self.ts = datetime.utcnow().timestamp()
        self.required_arguments = []
        self.module = module

    def define_argument(self, name):
        self.required_arguments.append(name)

    def get_arg(self, item):
        return self.request.get_arg(item)

    def set_exception(self, ex):
        self.request.set_error(ex)
        self.am.request_error(self.request)

    def set_return_value(self, value):
        self.request.set_return_value(value)

    @abc.abstractmethod
    def functionality(self):
        pass


class Callback(CallableObject):
    __metaclass__ = abc.ABCMeta
    """Base class for all callbacks to be executed on events"""
    # To be filled on child class
    name = 'callback'
    description = ""
    version = "0.0"

    def __init__(self, event, manager, module):
        CallableObject.__init__(self)
        self.event = event
        self.em = manager  # event manager
        self.module = module
        self.ts = datetime.utcnow().timestamp()

    @abc.abstractmethod
    def functionality(self):
        pass

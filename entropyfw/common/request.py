#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Lock
from entropyfw import get_utc_ts
from .logger import log

__author__ = 'otger'


class RequestStatus(object):
    created = 0
    error = 1
    done = 2


class UnknownCommand(Exception):
    pass


class Request(object):
    """Class to encapsulate requests of actions between modules
    """
    def __init__(self, command_id, source, target, command, arguments={}):
        """
        :param command_id: Command id assigned by generator of the command
        :param generator_id: client id of the module generating the petition
        :param target: module name of the module that must execute the command
        :param command: command to be executed
        :param arguments: arguments to command
        """
        self.created_ts = get_utc_ts()
        self.done_ts = None
        self.cmd_id = command_id
        self.source = source
        self.target = target
        self.command = command
        self.arguments = arguments
        self.return_value = None
        self.status = RequestStatus.created
        self.exception = None
        self.done_lock = Lock()
        self.done_lock.acquire()
        self.ack = False  # Could be a Condition

    def set_error(self, exc):
        self.exception = exc
        self.status = RequestStatus.error
        self._release()

    def set_return_value(self, ans):
        self.return_value = ans
        self.status = RequestStatus.done
        self._release()

    def _release(self):
        self.done_ts = get_utc_ts()
        try:
            self.done_lock.release()
        except Exception:
            log.debug("Exception when releasing Request lock")

    # def acknowledge(self):
    #     # ToDo: acknowledge, command has been received by target module
    #     self.ack = True

    def wait_answer(self, blocking=True, timeout=-1):
        #ToDo: adapt for py2
        self.done_lock.acquire(blocking=blocking, timeout=timeout)
        self.done_lock.release()
        return

    def elapsed(self):
        if self.done_ts:
            return self.done_ts - self.created_ts

    def get_arg(self, name):
        return self.arguments.get(name, None)
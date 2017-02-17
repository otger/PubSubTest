#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Lock
from pubsub import get_utc_ts

__author__ = 'otger'


class RequestStatus(object):
    created = 0
    error = 1
    done = 2


class UnknownCommand(Exception):
    pass


class Request(object):
    """Class to encapsulate commands between modules
    """
    def __init__(self, command_id, source_mod, target_mod, command, arguments={}):
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
        self.source_mod = source_mod
        self.target_mod = target_mod
        self.command = command
        self.arguments = arguments
        self.answer = None
        self.status = RequestStatus.created
        self.exception = None
        self.done_lock = Lock()
        self.done_lock.acquire()
        self.ack = False # Could be a Condition

    def set_error(self, exc):
        self.exception = exc
        self.status = RequestStatus.error
        self._release()

    def set_answer(self, ans):
        self.answer = ans
        self.status = RequestStatus.done
        self._release()

    def get_cmd_path(self):
        return '{0}.command'.format(self.target_mod)

    def _release(self):
        self.done_ts = get_utc_ts()
        try:
            self.done_lock.release()
        except:
            pass

    def acknowledge(self):
        # ToDo: acknowledge, command has been received by target module
        self.ack = True

    def wait_answer(self, blocking=True, timeout=-1):
        #ToDo: adapt for py2
        self.done_lock.acquire(blocking=blocking, timeout=timeout)
        self.done_lock.release()
        return

    def elapsed(self):
        if self.done_ts:
            return self.done_ts - self.created_ts

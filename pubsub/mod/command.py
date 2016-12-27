#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'otger'


class CommandStatus(object):
    created = 0
    error = 1
    done = 2

class UnknownCommand(Exception):
    pass


class Command(object):
    """Class to encapsulate commands between modules
    """
    def __init__(self, command_id, generator_mod, target_mod, command, arguments={}):
        """
        :param command_id: Command id assigned by generator of the command
        :param generator_id: client id of the module generating the petition
        :param target: module name of the module that must execute the command
        :param command: command to be executed
        :param arguments: arguments to command
        """
        self.cmd_id = command_id
        self.generator_mod = generator_mod
        self.target_mod = target_mod
        self.command = command
        self.arguments = arguments
        self.answer = None
        self.status = CommandStatus.created
        self.exception = None

    def set_error(self, exc):
        self.exception = exc
        self.status = CommandStatus.error

    def set_answer(self, ans):
        self.answer = ans
        self.status = CommandStatus.done

    def get_req_path(self):
        return '{0}.command'.format(self.target_mod)

    def get_ans_path(self):
        return '{0}.return.{1}'.format(self.generator_mod, self.cmd_id)

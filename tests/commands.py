#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from threading import Lock

from pubsub.dealer.dealer import Dealer
from pubsub.mod.modbase import ModBase
from pubsub.mod.command import UnknownCommand

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB = True
except ImportError:
    MATPLOTLIB = False
try:
    from scipy import stats
    SCIPY = True
except ImportError:
    SCIPY = False

__author__ = 'otger'


class Caller(ModBase):
    def __init__(self, dealer):
        ModBase.__init__(self, dealer=dealer, root_name='caller')
        self.calls = 0

    def cmd_executer(self, cmd):
        """
        If we are at this level, cmd is a pubsub.mod.command.Command instance
        :param cmd: pubsub.mod.command.Command instance
        :return: must be cmd with filled values
        """
        cmd.set_error = UnknownCommand("command {0} not found on module".format(cmd.command))

    def ask_temperature(self):
        cmd = self.request_cmd(target_mod='executer', command='get_temp')
        print("Caller cmd id: {0}".format(id(cmd)))
        cmd.wait_answer()
        print('Answered: {0}'.format(cmd.answer))
        print('Elapsed: {0}'.format(cmd.elapsed()))


class Executer(ModBase):
    def __init__(self, dealer):
        ModBase.__init__(self, dealer=dealer, root_name='executer')
        self.calls = 0

    def cmd_executer(self, cmd):
        """
        If we are at this level, cmd is a pubsub.mod.command.Command instance
        :param cmd: pubsub.mod.command.Command instance
        :return: must be cmd with filled values
        """
        self.calls += 1
        print("Executer cmd id: {0}".format(id(cmd)))
        if cmd.command == "get_temp":
            cmd.set_answer(self.get_temperature(cmd.arguments))
        elif cmd.command == "pub_temps":
            cmd.set_answer(self.pub_temperatures(cmd.arguments))
        if cmd.command == "get_big":
            cmd.set_answer(self.get_bigsize(cmd.arguments))
        elif cmd.command == "pub_big":
            cmd.set_answer(self.pub_bigsize(cmd.arguments))
        else:
            cmd.set_error = UnknownCommand("command {0} not found on module".format(cmd.command))
        return cmd

    def get_temperature(self, args):
        print("executing get temp")
        return 273.15

    def pub_temperatures(self, args):
        num_of_values = args['iterations']
        for i in range(num_of_values):
            self.publish('sensors.temperatures', i)

    def get_bigsize(self, args):
        num_of_bytes = args['size']
        return b''.join([b'a' for _ in range(num_of_bytes)])

    def pub_bigsize(self, args):
        num_of_bytes = args['size']
        retval = b''.join([b'a' for _ in range(num_of_bytes)])

        self.publish('data.bigsize', retval)

if __name__ == "__main__":

    d = Dealer()
    caller = Caller(dealer=d)
    executer = Executer(dealer=d)

    caller.ask_temperature()

    caller.exit()
    executer.exit()
    d.close()


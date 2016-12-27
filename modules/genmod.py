#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsub.mod.modbase import ModBase
from pubsub.mod.command import UnknownCommand
import threading
import time

__author__ = 'otger'


class GenericModule(ModBase):
    def __init__(self, dealer, rootname):
        super(GenericModule, self).__init__(dealer=dealer, rootname=rootname)
        self.calls = 0
        self.pub_loop_interval = 0.1
        self.pub_loop_samples = 1
        self._pub_loop_t = None
        self._pub_loop_exit = False

    def cmd_executer(self, cmd):
        """
        If we are at this level, cmd is a pubsub.mod.command.Command instance
        :param cmd: pubsub.mod.command.Command instance
        :return: must be cmd with filled values
        """
        self.calls += 1
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

    # Methods that implement commands

    @staticmethod
    def get_temperature(args):
        return args

    def pub_temperatures(self, args):
        num_of_values = args['iterations']
        for i in range(num_of_values):
            self.publish('sensors.temperatures', i)

    @staticmethod
    def get_bigsize(args):
        num_of_bytes = args['size']
        return b''.join([b'a' for _ in range(num_of_bytes)])

    def pub_bigsize(self, args):
        num_of_bytes = args['size']
        retval = b''.join([b'a' for _ in range(num_of_bytes)])

        self.publish('data.bigsize', retval)

    # External access methods just for proof of concept

    def ask_temperature(self, module_index, ):
    def start_pub_loop(self):
        if self._pub_loop_t is None:
            self._pub_loop_exit = False
            self._pub_loop_t = threading.Thread(target=self._pub_loop)
            self._pub_loop_t.start()

    def stop_pub_loop(self):
        self._pub_loop_exit = True
        if self._pub_loop_t is not None:
            self._pub_loop_t.join()
        self._pub_loop_t = None

    def _pub_loop(self):
        while self._pub_loop_exit is False:
            time.sleep(self.pub_loop_interval)

            for i in range(self.pub_loop_samples):
                self.publish('sensors.temperature.{0}'.format(i), 273.15 + i)









#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsub.mod.modbase import ModBase
from pubsub.mod.command import UnknownCommand
import threading
import time

__author__ = 'otger'


class GenericThread(object):
    def __init__(self, target):
        self.t = threading.Thread(target=target, args=[self])
        self.exit = False

    def start(self):
        self.exit = False
        self.t.start()

    def stop(self):
        self.exit = True
        self.t.join()


class GenericModule(ModBase):
    def __init__(self, dealer, root_name):
        super(GenericModule, self).__init__(dealer=dealer, root_name=root_name)
        self.calls = 0
        self.received_sensors = 0
        self.sensors = {}

        self.flood = GenericThread(target=self._flood)
        self.flood_samples = 10000

        self.pub_loop = GenericThread(target=self._pub_loop)
        self.pub_loop_interval = 0.001
        self.pub_loop_samples = 5

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

    def ask_temperature(self, module_name):
        return self.request_cmd(target_mod=module_name, command='get_temp')

    def _pub_loop(self, gt):
        while gt.exit is False:
            time.sleep(self.pub_loop_interval)
            for i in range(self.pub_loop_samples):
                self.publish('sensors.temperature.{0}'.format(i), 273.15 + i)

    def _sensors_callback(self, pqv):
        self.received_sensors += 1
        if pqv.publisher not in self.sensors:
            self.sensors[pqv.publisher] = 0
        self.sensors[pqv.publisher] += 1

    def subscribe_to(self, module, path='sensors'):
        # self.sensors[module] = 0
        self.subscribe(callback=self._sensors_callback, pattern='{0}.{1}'.format(module, path))

    def _flood(self, gt):
        start = time.time()
        for i in range(self.flood_samples):
            self.publish('sensors.flood', i)
        print("{0} - Elapsed {1} seconds to publish {2} samples".format(self.name,
                                                                        time.time()-start,
                                                                        self.flood_samples))








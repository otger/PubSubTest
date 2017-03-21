#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading

from old.modules import GenericModule
from pubsuber.dealer.dealer import Dealer

__author__ = 'otger'


class PubSubTest(object):
    def __init__(self, num_of_modules=10):
        self.dealer = Dealer()
        self.modules = []
        self.module_names = []
        for i in range(num_of_modules):
            self.modules.append(GenericModule(dealer=self.dealer,
                                              root_name='module.{0}'.format(i)))
            self.module_names.append('module.{0}'.format(i))


class TimerClass(threading.Thread):
    def __init__(self, target, interval, iterations=0):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.iterations = iterations
        self.count = 1
        self.interval = interval
        self.target = target

    def run(self):
        while self.count != self.iterations and not self.event.is_set():
            self.target()
            self.event.wait(self.interval)

    def stop(self):
        self.event.set()

if __name__ == "__main__":
    import time

    import logging
    from pubsuber.logger import log, formatter

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)


    start = time.time()
    NUM_OF_MODULES = 2
    pst = PubSubTest(NUM_OF_MODULES)

    def print_status():
        print("{0:.3f}".format(time.time() - start))
        for m in pst.modules:
            print("{0} - qsize: {1} - pub qsize: {2}".format(m.name, m.queue_size, m.push_queue_size))
            print("{0} - pubstats: {1} - stats: {2}".format(m.name, m.pub_stats, m.sensors))
        print()

    # Start thread that prints info once per second
    t = TimerClass(target=print_status, interval=1)
    t.start()

    for mod in pst.modules:
        for mod2 in pst.modules:
            if mod.name != mod2.name:
                mod.subscribe_to(mod2.name)
    # for mod in pst.modules:
    #     mod.pub_loop.start()
    #
    # time.sleep(5)
    #
    # for mod in pst.modules:
    #     print("{0} - Stopping publication".format(mod.name))
    #     mod.pub_loop.stop()

    for mod in pst.modules:
        mod.flood_samples = 100000
        mod.flood.start()

    for mod in pst.modules:
        mod.flood.stop()

    time.sleep(3)

    for mod in pst.modules:
        mod.exit()
    pst.dealer.close()
    t.stop()
    print_status()

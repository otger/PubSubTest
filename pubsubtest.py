#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsub.dealer.dealer import Dealer
from modules.genmod import GenericModule

__author__ = 'otger'


class PubSubTest(object):
    def __init__(self, num_of_modules=10):
        self.dealer = Dealer()
        self.modules = []
        self.module_names = []
        for i in range(num_of_modules):
            self.modules.append(GenericModule(dealer=self.dealer,
                                              rootname='module.{0}'.format(i)))
            self.module_names.append('module.{0}'.format(i))


if __name__ == "__main__":
    import time

    NUM_OF_MODULES = 5
    pst = PubSubTest(NUM_OF_MODULES)

    for mod in pst.modules:
        mod.start_pub_loop()
        for mod2 in pst.modules:
            if mod.name != mod2.name:
                mod.subscribe_to(mod2.name)

    time.sleep(5)
    for mod in pst.modules:
        print("{0} - Stopping publication".format(mod.name))
        mod.stop_pub_loop()
        mod.exit()
        print("{0} - stats: {1}".format(mod.name, mod.sensors))
        print("{0} - pubstats: {1}".format(mod.name, mod.pub_stats))


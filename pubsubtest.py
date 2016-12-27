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


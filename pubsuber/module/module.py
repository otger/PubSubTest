#!/usr/bin/python
# -*- coding: utf-8 -*-
from common.event import
__author__ = 'otger'


class Module(object):

    def __init__(self, name, dealer):
        self.name = name
        self.dealer = dealer
        self.eventmanager = EventManager(parent=self)

    def set_dealer(self, dealer):
        self.dealer = dealer


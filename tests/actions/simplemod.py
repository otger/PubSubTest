#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Module
from .action import Addition

__author__ = 'otger'


class SimpleModule(Module):
    name = 'simplemod'

    def __init__(self, dealer, name=None):
        Module.__init__(self, name=name, dealer=dealer)
        self.register_action(Addition)





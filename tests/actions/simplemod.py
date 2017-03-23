#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Module
from .action import Addition

__author__ = 'otger'


class SimpleModule(Module):
    def __init__(self, name, dealer):
        Module.__init__(self, name=name, dealer=dealer)
        self.register_action(Addition)





#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsuber.module.module import Module


__author__ = 'otger'


class SimpleModule(Module):
    def __init__(self, dealer):
        Module.__init__(self, dealer=dealer)




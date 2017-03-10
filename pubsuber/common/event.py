#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsuber import get_utc_ts

__author__ = 'otger'


class Event(object):
    def __init__(self, path):
        self.path = path
        self.value = None
        self.ts = get_utc_ts()
        self.source = None

    def set_source(self, module):
        self.source = module.name

    def set_value(self, value):
        self.value = value
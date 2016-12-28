#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsub import get_utc_ts

__author__ = 'otger'


class QueueValue(object):
    def __init__(self, publisher, path, value):
        self.publisher = publisher
        self.path = path
        self.value = value
        self.created_ts = get_utc_ts()



#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'otger'


class PubQueueValue(object):
    def __init__(self, clientid, path, value):
        self.clientid = clientid
        self.path = path
        self.value = value


#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'otger'


class PubQueueValue(object):
    def __init__(self, genclientid, path, value):
        self.genclientid = genclientid
        self.path = path
        self.value = value


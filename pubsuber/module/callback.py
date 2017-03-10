#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from threading import Lock

__author__ = 'otger'


class Callback(object):
    def __init__(self, index, callback, pattern, flags):
        self.ix = index
        self.function = callback
        self.pattern = pattern
        self.flags = flags
        self.re = re.compile(pattern, flags)
        self.subscription = None

    def set_subscription(self, subscription):
        self.subscription = subscription


class Callbacks(object):
    def __init__(self):
        self._cbs = []
        self._idx = 0
        # self._l = Lock()

    def add_cb(self, callback, pattern, flags):
        # with self._l:
        self._idx += 1
        cb = Callback(self._idx, callback, pattern, flags)
        self._cbs.append(cb)
        return cb

    def rem_cb(self, index):
        # with self._l:
        self._cbs = [x for x in self._cbs if x.index != index]

    def get_matches(self, path):
        # self._l.acquire()
        # try:
        #     ret = [x for x in self._cbs if x.re.match(path)]
        # finally:
        #     self._l.release()
        # with self._l:
        ret = [x for x in self._cbs if x.re.match(path)]
        return ret

    def __len__(self):
        return len(self._cbs)
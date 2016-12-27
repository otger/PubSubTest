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


class Callbacks(object):
    def __init__(self):
        self._cbs = []
        self._idx = 0
        self._l = Lock()

    def add_cb(self, callback, pattern, flags):
        self._l.acquire()
        try:

            self._idx += 1
            cb = Callback(self._idx, callback, pattern, flags)
            self._cbs.append(cb)
        finally:
            self._l.release()
        return cb

    def rem_cb(self, index):
        self._l.acquire()
        try:
            self._cbs = [x for x in self._cbs if x.index != index]
        finally:
            self._l.release()

    def get_matches(self, path):
        self._l.acquire()
        try:
            ret = [x for x in self._cbs if x.re.match(path)]
        finally:
            self._l.release()
        return ret

    def __len__(self):
        return len(self._cbs)
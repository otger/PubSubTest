#!/usr/bin/python
# -*- coding: utf-8 -*-
import uuid
import re
from .logger import log

__author__ = 'otger'


class Subscription(object):
    def __init__(self, callback, pattern, flags=0):
        self.uuid = uuid.uuid4()
        self.callback = callback
        self.pattern = pattern
        self.flags = flags
        self.re = re.compile(pattern, flags)

    def match(self, path):
        return self.re.match(path)

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __ne__(self, other):
        return self.uuid != other.uuid


class CallbacksSubscriptions(object):
    def __init__(self):
        self.subs = []

    def add(self, callback, pattern, flags=0):
        # with self._l:
        subscription = Subscription(callback, pattern, flags)
        self.subs.append(subscription)
        return subscription

    def remove(self, subscription):
        # with self._l:
        self.subs = [x for x in self.subs if subscription != x]

    def get_event_subscriptions(self, event):
        ans = [s for s in self.subs if s.match(event.full_id)]
        return ans

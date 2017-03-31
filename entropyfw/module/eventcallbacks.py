#!/usr/bin/python
# -*- coding: utf-8 -*-

from .callables import Callback
from .subscriptions import CallbacksSubscriptions
from .logger import log
from .interncallbacks import Exit
__author__ = 'otger'


class EventCallbacks(object):
    def __init__(self, module):
        self.module = module
        self.subs = CallbacksSubscriptions()
        self.history = []
        self.request_errors = []

        # Register internal events
        self.register_callback(Exit, 'dealer.exit')

    def register_callback(self, callback, pattern, flags=0):
        if not issubclass(callback, Callback):
            raise TypeError("callback must be a class which inherits from Callback")
        self.subs.add(callback, pattern, flags)
        log.debug("Registered callback {0} for pattern '{1}'".format(callback.name, pattern))

    def check_event(self, event):
        # requested_command = request.command
        subs = self.subs.get_event_subscriptions(event)
        for s in subs:
            self.module.worker.put_callback(s.callback.get_cb(event, self, self.module))


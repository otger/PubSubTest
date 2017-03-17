#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue
from pubsuber.dealer.dealerclient import DealerClient
from .subscriptions import SubscriptionsManager
from .worker import Worker
from .logger import log
__author__ = 'otger'


class Module(DealerClient):

    def __init__(self, name, dealer):
        super(Module).__init__(dealer=dealer, name=name)
        self._in_queue = queue.Queue()
        self._subs = SubscriptionsManager()
        self._worker = Worker(queue=self._in_queue)
        self._internal_events_register()

    def check_event(self, event):
        """Dealer client abstract method
        When dealer receives a new event it distributes it to all clients who must check if it has a subscription to it and add to its own queue
        """
        subs = self._subs.check_event(event)
        for s in subs:
            self._in_queue.put((s, event))

    def register_event(self, callback, pattern, flags=0):
        self._subs.add(callback, pattern, flags)

    def _exit_callback(self, event):
        self._worker.exit = True
        log.debug("Module {0} exiting".format(self.name))

    def _internal_events_register(self):
        self.register_event(self._exit_callback, 'dealer.exit')

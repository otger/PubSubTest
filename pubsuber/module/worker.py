#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
import queue
from .logger import log
__author__ = 'otger'


class Worker(Thread):
    def __init__(self):
        self.q = queue.Queue()
        self.exit = False
        super(Worker).__init__(self)

    def run(self):
        while not self.exit:
            (subscription, event) = self.q.get()
            try:
                subscription.callback(event)
            except Exception:
                log.exception("Exception processing event callback")
        log.info("Module worker exiting")





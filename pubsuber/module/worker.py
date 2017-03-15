#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'otger'


class Worker(Thread):
    def __init__(self, eventmanager):
        self.em = eventmanager
        self.dc = eventmanager.dc
        self.exit = False
        super(Worker).__init__(self)

    def run(self):
        while True:
            ev = self.dc.q.get()
            cbs = self.em.callbacks.get_matches(ev)
            for c in cbs:
                try:
                    c.function(ev)
                except Exception as ex:
                    # log.exception()
                    pass
        # log.info("Queue worker exiting")


    def stop(self):



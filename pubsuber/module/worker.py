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
            if ev is True:
                continue
            # we got some update as a QueueValue
            # Find which _cbs met the pattern:
            cbs = self.em.callbacks.get_matches(pqv.path)
            for c in cbs:
                try:
                    c.function(pqv)
                except Exception as ex:
                    # log.exception()
                    pass
            self._dc.q.task_done()
        # log.info("Queue worker exiting")


    def stop(self):



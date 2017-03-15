#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
from .logger import log
from pubsuber.common.event import Event

__author__ = 'otger'


class Worker(Thread):
    def __init__(self, dealer):
        self.dealer = dealer
        self.exit = False
        super(Worker).__init__(self)

    def run(self):
        while not self.exit:
            ev = self.dealer.in_queue.get()
            try:
                if not isinstance(ev, Event):
                    log.warning("A non Event object has been received at dealer: {0}".format(ev))
                else:
                    for c in self.dealer.clientmanager:
                        c.check_event(ev)
            except Exception:
                log.exception("Exception happened when processing event at dealer")
            finally:
                self.dealer.in_queue.task_done()






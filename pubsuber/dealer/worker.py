#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
import queue
from .logger import log
from pubsuber.common.event import Event
from pubsuber.common.request import Request
from pubsuber.common.exceptions import UnknownPlayer

__author__ = 'otger'


class Worker(Thread):
    def __init__(self, dealer):
        self._in_queue = queue.Queue()
        self.dealer = dealer
        self.exit = False
        super(Worker).__init__(self)

    def run(self):
        while not self.exit:
            qv = self._in_queue.get()
            try:
                if isinstance(qv, Event):
                    for c in self.dealer.players:
                        c.check_event(qv)
                elif isinstance(qv, Request):
                    target = self.dealer.players[qv.target]
                    if target:
                        target.check_request(qv)
                    else:
                        qv.set_error(UnknownPlayer("Player '{0}' not in system".format(qv.target)))
                else:
                    log.warning("Dealer only deals with Events and Requests. Received: {0}".format(qv))

            except Exception:
                log.exception("Exception happened when processing event at dealer")
            finally:
                self.dealer.event_queue.task_done()

    def put(self, qv):
        """
        Add a value to queue
        :param qv: queue value. It must be either an Event or a Request
        :return:
        """
        self._in_queue.put(qv)


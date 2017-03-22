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
        self._exit = False
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                qv = self._in_queue.get(block=True, timeout=1)
            except queue.Empty:
                log.debug('Empty queue at dealer')
                if self._exit:
                    log.info('Exiting dealer worker thread')
                    break
            else:
                try:
                    if isinstance(qv, Event):
                        log.debug('Processing event {0} at dealer worker'.format(qv.full_id))
                        for c in self.dealer.players:
                            c.check_event(qv)
                    elif isinstance(qv, Request):
                        target = self.dealer.players[qv.target]
                        log.debug('Processing request for {0} at dealer worker'.format(target))
                        if target:
                            target.check_request(qv)
                        else:
                            qv.set_error(UnknownPlayer("Player '{0}' not in system".format(qv.target)))
                            log.error('Received request for unknown player')
                    else:
                        log.warning("Dealer only deals with Events and Requests. Received: {0}".format(qv))

                except Exception:
                    log.exception("Exception happened when processing event at dealer")
                finally:
                    self._in_queue.task_done()
        log.info("Dealer worker exiting")


    def put(self, qv):
        """
        Add a value to queue
        :param qv: queue value. It must be either an Event or a Request
        :return:
        """
        self._in_queue.put(qv)

    def exit(self):
        self._exit = True
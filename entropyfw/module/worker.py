#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
import queue
from .logger import log
__author__ = 'otger'


class Worker(Thread):
    def __init__(self):
        self.q = queue.Queue()
        self._exit = False
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                call_obj = self.q.get(block=True, timeout=1)
            except queue.Empty:
                # log.debug('Empty queue')
                if self._exit:
                    log.info('Exiting worker thread')
                    break
            else:
                try:
                    call_obj.run()
                except:
                    log.exception("Exception on module worker")
                finally:
                    self.q.task_done()
        log.info("Module worker exiting")

    def exit(self):
        self._exit = True

    def put_action(self, action):
        self.q.put(action)

    def put_callback(self, callback):
        self.q.put(callback)

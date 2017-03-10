#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue
from threading import Thread

from .subscriptions import SubscriptionsManager

__author__ = 'otger'





class Dealer (object):
    """
    It opens a queue for each one of the clients connected. Dealer has a queue (push queue)
    that it has to be used by clients to publish values.
     Clients receive subscribed values through its own qm
    """
    def __init__(self):
        self._push_queue = queue.Queue()
        self._exit = False
        self.qm = QueuesManager()
        self.sm = SubscriptionsManager()
        self._t = Thread(target=self._push_queue_worker)
        self._t.start()

    def close(self):
        self._exit = True
        self._push_queue.put(True)
        self._t.join()

    def get_push_queue(self):
        return self._push_queue

    def new_client(self, name):
        return self.qm.new_client(name)

    def remove_client(self, name):
        self.qm.remove_client(name)

    def get_client_queue(self, name):
        return self.qm.get_queue(name)

    def subscribe(self, subscriber_name, pattern, flags=0):
        """
        Subscribe a client to all paths that match pattern
        :param subscriber_name: subscriber name of the module
        :param pattern: pattern to subscribe to
        :param flags: flags of the regular expression
        :return: pubsub.dealer.Subscription instance. Required to unsubscribe
        """
        return self.sm.add_subs(subscriber_name, pattern, flags)

    def unsubscribe(self, subscription):
        self.sm.rem_subs(subscription)

    def _push_queue_worker(self):
        while self._exit is False:
            # While True used to empty queue before checking _exit value
            qv = self._push_queue.get()
            if qv is True:
                continue
            # A QueueValue has been received, it must be delivered
            clients = self.sm.filter_by_path(qv.path)
            self.qm.put(clients, qv)
            self._push_queue.task_done()




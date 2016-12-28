#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue
import uuid
import re
from threading import Lock, Thread
from .queuevalue import QueueValue

__author__ = 'otger'


class Subscription(object):
    def __init__(self, subscriber, pattern, flags=0):
        self.uuid = uuid.uuid4()
        self.subscriber = subscriber
        self.pattern = pattern
        self.flags = flags
        self.re = re.compile(pattern, flags)

    def match(self, path):
        return self.re.match(path)

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __ne__(self, other):
        return self.uuid != other.uuid


class Subscriptions(object):
    def __init__(self):
        # self._l = Lock()
        self.by_client = {}

    def add_subs(self, subscriber, pattern, flags=0):
        # with self._l:
        subscription = Subscription(subscriber, pattern, flags)
        if subscriber not in self.by_client:
            self.by_client[subscriber] = []
        self.by_client[subscriber].append(subscription)

        return subscription

    def rem_subs(self, subscription):
        # with self._l:
        if subscription.subscriber in self.by_client:
            self.by_client[subscription.subscriber] = [x for x in self.by_client[subscription.subscriber] if subscription != x]

    def filter_by_path(self, path):
        """
        Return all client id which its subscriptions match path
        :param path: path to be checked against all clients regular expressions (until a match is found)
        :return: list of client names, can be empty
        """
        # self._l.acquire()
        # ans = []
        # try:
        #     ans = [k for k in self.by_client.keys() if len([x for x in self.by_client[k] if x.match(path)])]
        # finally:
        #     self._l.release()
        # with self._l:
        ans = [k for k in self.by_client.keys() if len([x for x in self.by_client[k] if x.match(path)])]
        return ans

    def remove_client(self, name):
        # with self._l:
        if name in self.by_client:
            self.by_client.pop(name)


class Queues(object):
    def __init__(self):
        self.clients = {}
        self._clients_counter = 0

    def new_client(self, name):
        self._clients_counter += 1
        q = queue.Queue()
        if name in self.clients:
            raise Exception("Client already exists")
        self.clients[name] = q
        return q

    def remove_client(self, name):
        if name in self.clients:
            q = self.clients.pop(name)
            del q

    def get_queue(self, name):
        if name in self.clients:
            return self.clients[name]

    def put(self, clients, value):
        for k in clients:
            if k in self.clients:
                self.clients[k].put(value)


class Dealer (object):
    """
    It opens a queue for each one of the clients connected. Dealer has a queue (push queue)
    that it has to be used by clients to publish values.
     Clients receive subscribed values through its own queues
    """
    def __init__(self):
        self._push_queue = queue.Queue()
        self._exit = False
        self.queues = Queues()
        self.subs = Subscriptions()
        self._t = Thread(target=self._push_queue_worker)
        self._t.start()

    def close(self):
        self._exit = True
        self._t.join()

    def get_push_queue(self):
        return self._push_queue

    def new_client(self, name):
        return self.queues.new_client(name)

    def remove_client(self, name):
        self.queues.remove_client(name)

    def get_client_queue(self, name):
        return self.queues.get_queue(name)

    def subscribe(self, subscriber_name, pattern, flags=0):
        """
        Subscribe a client to all paths that match pattern
        :param subscriber_name: subscriber name of the module
        :param pattern: pattern to subscribe to
        :param flags: flags of the regular expression
        :return: pubsub.dealer.Subscription instance. Required to unsubscribe
        """
        return self.subs.add_subs(subscriber_name, pattern, flags)

    def unsubscribe(self, subscription):
        self.subs.rem_subs(subscription)

    def _push_queue_worker(self):
        while self._exit is False:
            try:
                while True:
                    # While True used to empty queue before checking _exit value
                    qv = self._push_queue.get(block=False, timeout=1)
                    # A QueueValue has been received, it must be delivered
                    clients = self.subs.filter_by_path(qv.path)
                    self.queues.put(clients, qv)
                    self._push_queue.task_done()
            except queue.Empty:
                continue



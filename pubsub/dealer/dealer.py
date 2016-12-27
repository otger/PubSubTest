#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue
import uuid
import re
from threading import Lock
from . import PubQueueValue

__author__ = 'otger'


class Subscription(object):
    def __init__(self, clientid, pattern, flags=0):
        self.uuid = uuid.uuid4()
        self.clientid = clientid
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
        self._l = Lock()
        self.by_client = {}

    def add_subs(self, clientid, pattern, flags=0):
        self._l.acquire()
        try:
            subscription = Subscription(clientid, pattern, flags)
            if clientid not in self.by_client:
                self.by_client[clientid] = []
            self.by_client[clientid].append(subscription)
        finally:
            self._l.release()

        return subscription

    def rem_subs(self, subscription):
        self._l.acquire()
        try:
            if subscription.clientid in self.by_client:
                self.by_client[subscription.clientid] = [x for x in self.by_client[subscription.clientid] if subscription != x]
        finally:
            self._l.release()

    def filter_by_path(self, path):
        """
        Return all client id which its subscriptions match path
        :param path: path to be checked against all clientids regular expressions (until a match is found)
        :return: list of clientids, can be empty
        """
        self._l.acquire()
        ans = []
        try:
            ans = [k for k in self.by_client.keys() if len([x for x in self.by_client[k] if x.match(path)])]
        finally:
            self._l.release()
        return ans

    def remove_client(self, clientid):
        self._l.acquire()
        try:
            if clientid in self.by_client:
                self.by_client.pop(clientid)
        finally:
            self._l.release()


class Queues(object):
    def __init__(self):
        self.clients = {}

    def new_client(self):
        clientid = uuid.uuid4()
        q = queue.Queue()
        self.clients[clientid] = q
        return clientid

    def remove_client(self, clientid):
        if clientid in self.clients:
            q = self.clients.pop(clientid)
            del q

    def get_queue(self, clientid):
        getattr(self.clients, clientid)

    def put(self, clientids, value):
        for k in clientids:
            if k in self.clients:
                self.clients[k].put(value)


class Dealer (object):
    def __init__(self):
        self.queues = Queues()
        self.subs = Subscriptions()

    def new_client(self):
        return self.queues.new_client()

    def remove_client(self, clientid):
        self.queues.remove_client(clientid)

    def get_client_queue(self, clientid):
        return self.queues.get_queue(clientid)

    def subscribe(self, clientid, pattern, flags=0):
        """
        Subscribe a clientid to all paths that match pattern
        :param clientid: clientid of the module
        :param pattern: pattern to subscribe to
        :param flags: flags of the regular expression
        :return: pubsub.dealer.Subscription instance. Required to unsubscribe
        """
        return self.subs.add_subs(clientid, pattern, flags)

    def unsubscribe(self, subscription):
        self.subs.rem_subs(subscription)


    def publish(self, clientid, path, value):
        clients = self.subs.filter_by_path(path)
        self.queues.put(clients, PubQueueValue(clientid, path, value))

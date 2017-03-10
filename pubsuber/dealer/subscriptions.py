#!/usr/bin/python
# -*- coding: utf-8 -*-
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


class SubscriptionsManager(object):
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

#!/usr/bin/python
# -*- coding: utf-8 -*-
from .queuevalue import QueueValue
__author__ = 'otger'


class DealerClient(object):

    def __init__(self, dealer, root_name):
        self.d = dealer
        self._name = root_name
        self.push_queue = dealer.get_push_queue()
        self.q = dealer.new_client(root_name)

    def sub(self, pattern, flags=0):
        return self.d.subscribe(self._name, pattern, flags)

    def unsub(self, subscription):
        self.d.unsubscribe(subscription)

    def pub(self, path, value):
        qv = QueueValue(publisher=self._name, path=path, value=value)
        self.push_queue.put(qv)
        # self.d.publish(self.cid, path, value)

    def remove(self):
        self.d.remove_client(self.cid)

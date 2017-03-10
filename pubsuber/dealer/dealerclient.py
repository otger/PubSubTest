#!/usr/bin/python
# -*- coding: utf-8 -*-
from common.event import Event
__author__ = 'otger'


class DealerClient(object):

    def __init__(self, module):
        self.mod = module
        self.d = module.dealer
        self._name = module.name
        self.push_queue = self.d.get_push_queue()
        self.q = self.d.new_client(self._name)

    def sub(self, pattern, flags=0):
        return self.d.subscribe(self._name, pattern, flags)

    def unsub(self, subscription):
        self.d.unsubscribe(subscription)

    def pub(self, event):
        if not isinstance(event, Event):
            raise Exception('Values published in queues must be Event instances')
        self.push_queue.put(event)
        # self.d.publish(self.cid, path, value)

    def action_request(self, request):
        # Dealer client has separate paths for publish and to request commands. This way if a specific queue for
        # commands has to be implemented, only Dealer and DealerClient must be changed and will be transparent to
        # modules
        ev = Event(path='{0}.action'.format(request.target_mod))
        ev.set_value(request)
        ev.set_source(self.mod)
        self.push_queue.put(ev)

    def remove(self):
        self.d.remove_client(self.cid)

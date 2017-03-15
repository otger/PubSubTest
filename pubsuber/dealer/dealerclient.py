#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsuber.common.event import Event
import abc
__author__ = 'otger'


class DealerClient(metaclass=abc.ABCMeta):
    def __init__(self, dealer, name):
        self.d = dealer
        self.name = name
        self.d.new_client(self)

    def pub_event(self, event_id, value=None):
        event = Event(source=self.name, event_id=event_id, value=value)
        self.dealer.in_queue.put(event)

    def request_action(self, request):
        # Dealer client has separate paths for publish and to request commands. This way if a specific queue for
        # commands has to be implemented, only Dealer and DealerClient must be changed and will be transparent to
        # modules
        self.pub_event(event_id='{0}.action'.format(request.target_mod), value=request)

    @abc.abstractmethod
    def check_event(self, event):
        pass

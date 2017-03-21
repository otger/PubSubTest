#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsuber.common.event import Event
import abc
__author__ = 'otger'


class Player(metaclass=abc.ABCMeta):
    def __init__(self, dealer, name):
        self.d = dealer
        self.name = name
        self.d.add_player(self)

    def pub_event(self, event_id, value=None):
        event = Event(source=self.name, event_id=event_id, value=value)
        self.d.event(event)

    def request(self, request=None, command_id=None, target_mod=None):
        self.d.request(request)

    @abc.abstractmethod
    def check_event(self, event):
        """
        Module must check if it has a subscription to that event.
        If this is the case
        :param event:
        :return:
        """
        pass

    @abc.abstractmethod
    def check_request(self, request):
        """
        Module must implement a way to check if command of request is implemented
        :param request:
        :return:
        """
        pass
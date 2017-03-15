#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue
from pubsuber.common.event import Event
from .worker import Worker
from .clientmanager import ClientManager

__author__ = 'otger'


class Dealer (object):
    """
    It opens a queue for each one of the clients connected. Dealer has a queue (push queue)
    that it has to be used by clients to publish values.
     Clients receive subscribed values through its own qm
    """
    def __init__(self):
        self.in_queue = queue.Queue()
        self.clientmanager = ClientManager()
        self.w = Worker(self)
        self.w.start()

    def send_event(self, event_id, value=None):
        self.in_queue.put(Event(source='dealer', event_id=event_id, value=value))

    def exit(self):
        self.send_event('exit')
        self.w.exit = True
        self.w.join()

    def new_client(self, client):
        return self.clientmanager.new_client(client)

    def remove_client(self, client):
        return self.clientmanager.remove_client(client)


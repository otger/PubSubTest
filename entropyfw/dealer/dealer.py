#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw.common.event import Event
from entropyfw.common.request import Request
from .worker import Worker
from .playermanager import PlayerManager
from .logger import log
from .stats import DealerStats

__author__ = 'otger'


class Dealer (object):
    """
    Dealer has a queue (push queue) that it has to be used by players to publish values using dealer methods
     Clients receive subscribed values through its own qm
    """
    def __init__(self):
        self.worker = Worker(self)
        self.worker.start()
        self.players = PlayerManager()
        self.stats = DealerStats()
        log.debug('Created Dealer')

    def _pub_event(self, event_id, value=None):
        self.worker.put(Event(source='dealer', event_id=event_id, value=value))

    def exit(self):
        self._pub_event('exit')
        self.worker.exit()
        self.worker.join()

    def add_player(self, player):
        return self.players.add_player(player)

    def remove_player(self, player):
        return self.players.remove_player(player)

    def event(self, event):
        """
        Used by players to add an event to be dealt
        Events have information of sender but are not directed to a particular player, all of them receive the event

        :param event:
        :return:
        """
        if isinstance(event, Event):
            self.worker.put(event)
            self.stats.reg_event(event)

    def request(self, request):
        """
        Used by players to request something to another player
        Requests are directed to a particular player. Have "source" and "target" fields.

        :param request:
        :return:
        """
        if isinstance(request, Request):
            self.worker.put(request)
            # log.debug('Added request to dealer worker')
            self.stats.reg_req(request)

        return request

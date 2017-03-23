#!/usr/bin/python
# -*- coding: utf-8 -*-
from .logger import log

__author__ = 'otger'


class PlayerManager(object):
    def __init__(self):
        self._players = {}
        self._players_count = 0
        log.debug("Created players manager")

    def add_player(self, player):
        if player.name in self._players:
            log.error("Player with this name already exists: {0}".format(player.name))
            raise Exception("Player already exists")
        self._players[player.name] = player
        self._players_count += 1
        log.debug("Added new player to player manager: {0}".format(player.name))

    def remove_player(self, player):
        if player.name in self._players:
            self._players.pop(player.name)
            self._players_count -= 1
            log.debug("Removed player from player manager: {0}".format(player.name))

    def __iter__(self):
        for p in self._players.values():
            yield p

    def __getitem__(self, item):
        return self._players.get(item, None)

    def _get_num_players(self):
        return self._players_count
    num_players = property(_get_num_players)

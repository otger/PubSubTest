#!/usr/bin/python
# -*- coding: utf-8 -*-
from .logger import log

__author__ = 'otger'


class ClientManager(object):
    def __init__(self):
        self._clients = {}
        self._clients_counter = 0
        log.debug("Created dealer client manager")

    def new_client(self, client):
        if client.name in self.clients:
            log.error("Client with this name already exists: {0}".format(client.name))
            raise Exception("Client already exists")
        self.clients[client.name] = client
        self._clients_counter += 1
        log.debug("Added new dealer client to client manager: {0}".format(client.name))

    def remove_client(self, client):
        if client.name in self.clients:
            self.clients.pop(client.name)
            self._clients_counter -= 1
            log.debug("Removed dealer client from client manager: {0}".format(client.name))

    def __iter__(self):
        for k in self._clients:
            yield self._clients[k]

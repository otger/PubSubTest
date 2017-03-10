#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue

__author__ = 'otger'


class QueuesManager(object):
    def __init__(self):
        self.clients = {}
        self._clients_counter = 0

    def new_client(self, name):
        q = queue.Queue()
        if name in self.clients:
            raise Exception("Client already exists")
        self.clients[name] = q
        self._clients_counter += 1
        return q

    def remove_client(self, name):
        if name in self.clients:
            q = self.clients.pop(name)
            del q
            self._clients_counter -= 1

    def get_queue(self, name):
        if name in self.clients:
            return self.clients[name]

    def put(self, clients, value):
        for k in clients:
            if k in self.clients:
                self.clients[k].put(value)

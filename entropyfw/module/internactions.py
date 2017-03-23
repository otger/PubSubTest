#!/usr/bin/python
# -*- coding: utf-8 -*-
from .callables import Action

__author__ = 'otger'


class ListRegisteredActions(Action):
    name = 'listregisteredactions'
    arguments = []
    description = "Returns a list of tuples containing name, argument names, description and version of each defined action of a module"
    version = "0.1"

    def __init__(self, request, manager, module):
        Action.__init__(self, request, manager, module)

    def functionality(self):
        reg_actions = []
        for k, v in self.am.actions.items():
            reg_actions.append((v.name, v.arguments, v.description, v.version))

        return reg_actions



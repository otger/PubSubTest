#!/usr/bin/python
# -*- coding: utf-8 -*-
from .callables import Callback
from .logger import log

__author__ = 'otger'


class Exit(Callback):
    name = 'exit'
    description = "Closes worker thread"
    version = "0.0"

    def __init__(self, event, manager, module):
        Callback.__init__(self, event, manager, module)

    def functionality(self):
        self.module.worker.exit()
        log.debug("Module {0} exiting".format(self.module.name))

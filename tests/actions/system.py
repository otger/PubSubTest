#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import System
from .simplemod import SimpleModule
from entropyfw.common.request import Request

__author__ = 'otger'


class SystemActions(System):

    def __init__(self):
        System.__init__(self)
        self.add_module(SimpleModule(name='adder'))

    def sum(self, a, b):
        r = self.send_request(target='adder', command='addition',
                              arguments={'s1': a, 's2': b})
        return r

    def list_functionality(self):
        r = self.send_request(target='adder',
                    command='listregisteredactions')
        self.dealer.request(r)
        r.wait_answer()
        s = "Functionality of module 'adder': \n"
        for el in r.return_value:
            s += "\t - {0}\n".format(', '.join([str(x) for x in el]))
        print(s)
        return r

if __name__ == "__main__":
    from entropyfw.logger import log, formatter
    import logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    s = SystemActions()
    log.info('Created system')
    r = s.sum(1, 2)
    log.info('Asked int sum')
    log.info("Sum(1,2) returned: {0}".format(r.return_value))
    r.wait_answer()
    r = s.sum('a', 'b')
    log.info('Asked str sum')
    r.wait_answer()
    log.info("Sum('a', 'b') returned: {0}".format(r.return_value))
    s.list_functionality()

    s.exit()

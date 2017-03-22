#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsuber.dealer.dealer import Dealer
from .simplemod import SimpleModule
from pubsuber.common.request import Request
__author__ = 'otger'


class SystemActions(object):

    def __init__(self):
        self.dealer = Dealer()
        self.m1 = SimpleModule(name='adder', dealer=self.dealer)

    def exit(self):
        self.dealer.exit()

    def sum(self, a, b):
        r = Request(command_id=0,
                    source='myself',
                    target='adder',
                    command='addition',
                    arguments={'s1': a, 's2': b})
        self.dealer.request(r)
        # r.wait_answer()
        # print(r.return_value)
        return r

    def list_functionality(self):
        r = Request(command_id=0,
                    source='myself',
                    target='adder',
                    command='listregisteredactions')
        self.dealer.request(r)
        r.wait_answer()
        s = "Functionality of module 'adder': \n"
        for el in r.return_value:
            s += "\t - {0}\n".format(', '.join([str(x) for x in el]))
        print(s)
        return r

if __name__ == "__main__":
    from pubsuber.logger import log, formatter
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

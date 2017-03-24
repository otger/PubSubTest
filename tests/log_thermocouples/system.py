#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import Dealer
from entropyfw.common.request import Request
from s_pico_tc08.module import EntropyPicoTc08
from s_eventlogger.module import EntropyEventLogger
import time
"""
system
Created by otger on 23/03/17.
All rights reserved.
"""


class SystemTC08(object):

    def __init__(self):
        self.dealer = Dealer()
        self.tc08 = EntropyPicoTc08(dealer=self.dealer, channels=list(range(9)))
        self.log = EntropyEventLogger(dealer=self.dealer, print_data=True)
        self.log.add_log('{0}.temperatures'.format(self.tc08.name))

    def exit(self):
        self.dealer.exit()

    def pub_temps(self, interval):
        r = Request(command_id=0,
                    source='myself',
                    target='picotc08',
                    command='starttimer',
                    arguments={'interval': interval})
        self.dealer.request(r)
        # r.wait_answer()
        # print(r.return_value)
        return r

    def stop_pub_temps(self):
        r = Request(command_id=0,
                    source='myself',
                    target='picotc08',
                    command='stoptimer',
                    arguments={})
        self.dealer.request(r)
        # r.wait_answer()
        # print(r.return_value)
        return r

    def list_functionality(self):
        r = Request(command_id=0,
                    source='myself',
                    target='picotc08',
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

    s = SystemTC08()
    log.info('Created system')
    r = s.pub_temps(2)
    r.wait_answer()
    s.list_functionality()

    time.sleep(100)
    r = s.stop_pub_temps()
    log.info('Asked stop timer')
    r.wait_answer()

    s.log.save_file()
    time.sleep(5)
    s.exit()

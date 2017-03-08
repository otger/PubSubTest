#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

from pubsuber.dealer.dealer import Dealer
from tests.modules.genmod import GenericModule
from threading import Lock

__author__ = 'otger'


class CountDownModule(GenericModule):
    def __init__(self, dealer, count, pair, lead=False):
        self.lead_element = lead
        self.elementid = 0 if lead else 1
        self.partnerid = 1 if lead else 0
        self.pair = pair
        rootname = 'pair{0}.element{1}'.format(pair.pairid, self.elementid)
        GenericModule.__init__(self, dealer=dealer, root_name=rootname)

        self._count = count
        self.init_count = count

        self.pub_path = 'count'

        self.partnername = 'pair{0}.element{1}'.format(pair.pairid, self.partnerid)
        self.partner_pub_path = '{0}.count'.format(self.partnername)

        self.subscribe(self.cb, self.partner_pub_path)
        print('{0} subscribed to {1}'.format(self.name, self.partner_pub_path))

        self._start = time.time()

    def cb(self, pqv):
        value = pqv.value
        if self.lead_element and value <= 0:
            print("Pair {0} elapsed {1} seconds to countdown from {2}".format(self.pair.pairid, time.time()-self._start,
                                                                              self.init_count))
            self.pair.done()
        else:
            self.p(value-1)

    def start(self):
        self._start = time.time()
        self.p(self.init_count)

    def p(self, value):
        self.publish(self.pub_path, value)
        # print("{0} published {1}: {2}".format(self.name, self.pub_path, value))


class CountDownPair(object):
    def __init__(self, dealer, count, pairid):
        self.dealer = dealer
        self.pairid = pairid
        self.lead = CountDownModule(dealer=dealer, count=count, pair=self, lead=True)
        self.foll = CountDownModule(dealer=dealer, count=count, pair=self, lead=False)
        self._l = Lock()

    def start(self):
        self.lead.start()
        self._l.acquire()

    def stop(self):
        self.lead.exit()
        self.foll.exit()

    def done(self):
        self._l.release()

    def wait_done(self):
        self._l.acquire()


class CountDown(object):
    def __init__(self, count=1000, couples=1):
        self.dealer = Dealer()
        self.couples = []
        for i in range(couples):
            self.couples.append(CountDownPair(dealer=self.dealer,
                                              count=count,
                                              pairid=i))

    def start(self):
        for el in self.couples:
            el.start()

    def stop(self):
        for el in self.couples:
            el.stop()

    def wait_done(self):
        for el in self.couples:
            # print("Waiting on couple {0}".format(el.pairid))
            el.wait_done()
            el.done()



if __name__ == "__main__":

    c = CountDown(count=1000, couples=4)
    c.start()
    # time.sleep(4)
    # c.stop()
    # c.dealer.close()
    c.wait_done()
    c.stop()
    c.dealer.close()

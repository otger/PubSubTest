#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from threading import Lock

from old.modules import GenericModule
from entropyfw.dealer.dealer import Dealer

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB = True
except ImportError:
    MATPLOTLIB = False
try:
    from scipy import stats
    SCIPY = True
except ImportError:
    SCIPY = False

__author__ = 'otger'


class TValue(object):
    def __init__(self, value):
        self._init = time.time()
        self.value = value

    def _get_elapsed(self):
        return time.time() - self._init
    elapsed = property(_get_elapsed)

    def reset(self):
        self._init = time.time()


class DelayModule(GenericModule):
    def __init__(self, pair, count, pairid, lead=False):
        self.pair = pair
        self.lead_element = lead
        self.elementid = 0 if lead else 1
        self.partnerid = 1 if lead else 0
        self.pairid = pairid
        rootname = 'pair{0}.element{1}'.format(pairid, self.elementid)
        GenericModule.__init__(self, dealer=pair.dealer, root_name=rootname)

        self._count = count
        self.init_count = count

        self.pub_path = 'count'

        self.partnername = 'pair{0}.element{1}'.format(pairid, self.partnerid)
        self.partner_pub_path = '{0}.count'.format(self.partnername)

        self.subscribe(self.cb, self.partner_pub_path)
        self.delays = []
        print('{0} subscribed to {1}'.format(self.name, self.partner_pub_path))

        self._start = time.time()

    def cb(self, pqv):
        tvalue = pqv.value
        self.delays.append(tvalue.elapsed)
        if self.lead_element and tvalue.value <= 0:
            print("Pair {0} elapsed {1} seconds to countdown from {2}".format(self.pairid, time.time()-self._start,
                                                                              self.init_count))
            self.pair.done()
        else:
            tvalue.value -= 1
            tvalue.reset()
            self.p(tvalue)

    def start(self):
        self._start = time.time()
        self.p(TValue(self.init_count))

    def p(self, value):
        self.publish(self.pub_path, value)
        # print("{0} published {1}: {2}".format(self.name, self.pub_path, value))


class DelayPair(object):
    def __init__(self, dealer, count, pairid):
        self.dealer = dealer
        self.pairid = pairid
        self.lead = DelayModule(pair=self, count=count, pairid=pairid, lead=True)
        self.foll = DelayModule(pair=self, count=count, pairid=pairid, lead=False)
        self._l = Lock()

    def start(self):
        try:
            self._l.acquire(False)
        except Exception as ex:
            print(ex)
        self.lead.start()

    def stop(self):
        self.lead.exit()
        self.foll.exit()

    def done(self):
        try:
            self._l.release()
        except Exception as ex:
            print(ex)

    def wait_done(self):
        self._l.acquire(True)


class Delay(object):
    def __init__(self, count=1000, couples=1):
        self.dealer = Dealer()
        self.couples = []
        for i in range(couples):
            self.couples.append(DelayPair(dealer=self.dealer,
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
            el.wait_done()

if __name__ == "__main__":

    c = Delay(count=5000, couples=5)
    c.start()
    # time.sleep(4)
    # c.stop()
    # c.dealer.close()
    c.wait_done()
    c.stop()
    c.dealer.close()

    if MATPLOTLIB:
        for el in c.couples:
            a = el.lead.delays + el.foll.delays
            plt.hist(a, bins=100, alpha=0.5, label='Pair{0}'.format(el.pairid))
        plt.xlabel("Delay")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()
    if SCIPY:
        for el in c.couples:
            a = el.lead.delays + el.foll.delays
            print(stats.describe(a))

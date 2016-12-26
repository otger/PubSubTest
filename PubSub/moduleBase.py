from .dealerclient import DealerClient
from queue import Empty
import re
from threading import Lock, Thread



class Callback(object):
    def __init__(self, index, callback, pattern, flags):
        self.ix = index
        self.function = callback
        self.pattern = pattern
        self.flags = flags
        self.re = re.compile(pattern, flags)


class Callbacks(object):
    def __init__(self):
        self.callbacks = []
        self._idx = 0
        self._l = Lock()

    def add_cb(self, callback, pattern, flags):
        self._l.acquire()
        try:
            self._idx += 1
            self.callbacks.append(Callback(self._idx, callback, pattern, flags))
        finally:
            self._l.release()
        return self._idx

    def rem_cb(self, index):
        self._l.acquire()
        try:
            self.callbacks = [x for x in self.callbacks if x.index != index]
        finally:
            self._l.release()

    def get_matches(self, path):
        self._l.acquire()
        try:
            ret = [x for x in self.callbacks if x.re.match(path)]
        finally:
            self._l.release()
        return ret


class ModuleBase(object):

    def __init__(self, dealer, rootname):
        self._dc = DealerClient(dealer)
        self._root = rootname
        self.callbacks = Callbacks()
        self._exit = False
        self._queue_timeout = 0.1
        self._threads = []
        t = Thread(target=self._queue_worker)
        t.start()
        self._threads.append(t)

    def publish(self, path, value):
        """
        Publish a value to Dealer
        :param path: path of the variable, rootname is added in front
        :param value: any python valid value
        :return:
        """
        self._dc.pub('{0}.{1}'.format(self._root, path), value)

    def subscribe(self, callback, pattern, flags=0):
        """
        Subscribe pattern at Dealer
        :param callback: function to be executed. This function must accept a single argument of type PubQueueValue
        :param pattern:
        :param flags:
        :return:
        """
        self._dc.sub(pattern=pattern, flags=flags)
        self.callbacks.add_cb(callback, pattern, flags)

    def _queue_worker(self):
        while self._exit is False:
            try:
                pqv = self._dc.q.get(block=False, timeout=self._queue_timeout)
            except Empty:
                continue
            else:
                # we got some update as a PubQueueValue
                # Find which callbacks met the pattern:
                cbs = self.callbacks.get_matches(pqv.path)
                for c in cbs:
                    try:
                        c.function(pqv)
                    except Exception:
                        # log.exception()
                        pass
        # log.info("Queue worker exiting")
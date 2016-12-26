from .dealerclient import DealerClient


class ModuleBase(object):

    def __init__(self, dealer, rootname):
        self._dc = DealerClient(dealer)
        self._root = rootname
        self.callbacks = {}

    def subscribe(self, pattern, callback):

class DealerClient(object):

    def __init__(self, dealer):
        self.d = dealer
        self.cid = dealer.new_client()
        self.q = dealer.get_client_queue(self.cid)

    def sub(self, pattern, flags=0):
        self.d.subscribe(self.cid, pattern, flags)

    def pub(self, path, value):
        self.d.publish(self.cid, path, value)

    def remove(self):
        self.d.remove_client(self.cid)

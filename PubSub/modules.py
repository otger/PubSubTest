from .moduleBase import ModuleBase


class Test1(ModuleBase):
    def __init__(self, dealer):
        super(Test1, self).__init__(dealer=dealer, rootname='Test1')
        self.subscribe(self.callback_0, r'Test2')

    def callback_0(self, pqv):
        print('received: {0}'.format(pqv))


class Test2(ModuleBase):
    def __init__(self, dealer):
        super(Test2, self).__init__(dealer=dealer, rootname='Test2')
        self.subscribe(self.callback_0, r'Test1')

    def callback_0(self, pqv):
        print('received: {0}'.format(pqv))

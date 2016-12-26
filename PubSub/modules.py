from .moduleBase import ModuleBase


class Test1(ModuleBase):
    def __init__(self):
        super(Test1, self).__init__(rootname=Test1)

        self.sub(r'Test2\.')
    def
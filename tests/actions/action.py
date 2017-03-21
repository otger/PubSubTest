#!/usr/bin/python
# -*- coding: utf-8 -*-

from pubsuber.module.action import Action


class Addition(Action):
    name = 'addition'

    def __init__(self, parent, request):
        super(Addition).__init__(parent=parent, request=request)
        self.define_argument('s1')
        self.define_argument('s2')

    def functionality(self):
        s1 = self.get_arg('s1')
        s2 = self.get_arg('s2')

        if s1 is None or s2 is None:
            raise Exception("Empty operands, can't make addition")

        return s1+s2


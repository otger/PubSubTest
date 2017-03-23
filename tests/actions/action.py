#!/usr/bin/python
# -*- coding: utf-8 -*-

from entropyfw import Action


class Addition(Action):
    name = 'addition'
    arguments = ['s1', 's2']
    description = "Returns the addition of two arguments"
    version = "0.1"

    def functionality(self):
        s1 = self.get_arg('s1')
        s2 = self.get_arg('s2')

        if s1 is None or s2 is None:
            raise Exception("Empty operands, can't make addition")

        return s1+s2


#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
stats
Created by otger on 29/03/17.
All rights reserved.
"""


class DealerStats(object):
    def __init__(self):
        self.eventstats = {}
        self.reqstats = {}

    def reg_event(self, event):
        if event.full_id not in self.eventstats.keys():
            self.eventstats[event.full_id] = 0
        self.eventstats[event.full_id] += 1

    def reg_req(self, request):
        if request.full_id not in self.reqstats.keys():
            self.reqstats[request.full_id] = 0
        self.reqstats[request.full_id] += 1

    def get_stats(self):
        return {'events': self.eventstats.copy(),
                'requests': self.reqstats.copy()}

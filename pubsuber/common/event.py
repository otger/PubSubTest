#!/usr/bin/python
# -*- coding: utf-8 -*-
from pubsuber import get_utc_ts

__author__ = 'otger'


class Event(object):
    def __init__(self, source, event_id, value=None):
        self._event_id = event_id
        self._value = value
        self._ts = get_utc_ts()
        self._source = source

    def _get_full_id(self):
        return '{0}.{1}'.format(self._source, self._event_id)
    full_id = property(_get_full_id)

    def _get_event_id(self):
        return self._event_id
    event_id = property(_get_event_id)

    def _get_source(self):
        return self._source
    source = property(_get_source)

    def _get_ts(self):
        return self._ts
    ts = property(_get_ts)

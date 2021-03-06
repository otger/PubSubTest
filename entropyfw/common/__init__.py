#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time

__author__ = 'otger'


def get_utc_ts():
    now = datetime.datetime.utcnow()
    return time.mktime(now.timetuple()) + now.microsecond/1e6


def utc_ts_string(ts, strformat='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.utcfromtimestamp(ts).strftime(strformat)

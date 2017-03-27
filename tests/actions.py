#!/usr/bin/python
# -*- coding: utf-8 -*-

from actions.system import SystemActions
"""
actions
Created by otger on 27/03/17.
All rights reserved.
"""

if __name__ == "__main__":
    from entropyfw.logger import log, formatter
    import logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    s = SystemActions()
    log.info('Created system')
    r = s.sum(1, 2)
    log.info('Asked int sum')
    r.wait_answer()
    log.info("Sum(1,2) returned: {0}".format(r.return_value))
    r = s.sum('a', 'b')
    log.info('Asked str sum')
    r.wait_answer()
    log.info("Sum('a', 'b') returned: {0}".format(r.return_value))
    s.list_functionality()

    s.exit()

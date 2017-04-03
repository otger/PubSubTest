#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from entropyfw.logger import log
from entropyfw.module.web import EntropyBlueprint

"""
blueprints
Created by otger on 27/03/17.
All rights reserved.
"""


class SystemBlueprint(Blueprint):
    def set_sys_info(self, sys_info):
        self.sys_info = sys_info


def get_blueprints():
    sys_bp = SystemBlueprint('system', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/system/static')

    @sys_bp.route('/')
    def show():
        try:
            data = {'page_title': 'Entropy System'}
            return render_template('sys/base.html', globals=sys_bp.sys_info, data=data)
        except Exception:
            log.exception("Failed to load template")
            abort(404)

    return (sys_bp,)

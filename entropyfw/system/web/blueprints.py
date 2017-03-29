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
    sys_bp = SystemBlueprint('sys_bp', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/sys_bp/static')

    @sys_bp.route('/')
    def show():
        try:
            data = {'mod_names': sys_bp.sys_info.mod_names}
            return render_template('sys/base.html', data=data, name='perico')
        except Exception:
            log.exception("Failed to load template")
            abort(404)

    return (sys_bp,)

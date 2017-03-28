#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from entropyfw.system.web.blueprints import EntropyBlueprint

__author__ = 'otger'


def get_blueprint(mod_name):
    simple_page = EntropyBlueprint(mod_name, __name__,
                            template_folder='templates')

    @simple_page.route('/')
    def show():
        try:
            return render_template('pages/index.html', mod_name=mod_name, data=simple_page.global_data)
        except TemplateNotFound:
            abort(404)

    return simple_page
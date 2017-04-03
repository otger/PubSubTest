#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from entropyfw.system.web.blueprints import EntropyBlueprint

__author__ = 'otger'


def get_blueprint(mod_name):
    # simple_page = EntropyBlueprint(mod_name, __name__,
    #                                template_folder='templates')
    #
    # @simple_page.route('/')
    # def show():
    #     try:
    #         data = {'page_title': 'Entropy System'}
    #         return simple_page.render_template('pages/index.html', mod_name=mod_name, globals=simple_page.global_data)
    #     except TemplateNotFound:
    #         abort(404)

    simple_page = SimplePage(mod_name, __name__,
                             template_folder='templates')

    return simple_page


class SimplePage(EntropyBlueprint):

    def register_routes(self):
        self.add_url_rule('/', 'index', self.index)

    def index(self):
        try:
            data = {'page_title': 'Adder'}
            return self.render_template('pages/index.html', data=data)
        except TemplateNotFound:
            abort(404)

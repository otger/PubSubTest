#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

__author__ = 'otger'


def get_blueprint(mod_name):
    simple_page = Blueprint('simple_page', __name__,
                            template_folder='templates',
                            url_prefix='/{0}'.format(mod_name))

    @simple_page.route('/', defaults={'page': 'index'})
    @simple_page.route('/<page>')
    def show(page):
        try:
            return render_template('pages/%s.html' % page, module=mod_name)
        except TemplateNotFound:
            abort(404)

    return simple_page
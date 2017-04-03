#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from urllib.parse import quote

"""
blueprints
Created by otger on 27/03/17.
All rights reserved.
"""


class ModuleWebManager(object):
    def __init__(self, parent):
        self.sys_info = None
        self.parent = parent
        self.blueprints = []
        self.api_resources = []

    def set_sys_info(self, sys_info):
        self.sys_info = sys_info
        for bp in self.blueprints:
            bp.set_sys_info(self.sys_info)

    def register_blueprint(self, blueprint):
        blueprint.set_mod_parent(self.parent)
        blueprint.set_sys_info(self.sys_info)
        self.blueprints.append(blueprint)

    def get_blueprints(self):
        return self.blueprints

    def register_api_resource(self, resource):
        self.api_resources.append(resource)

    def get_api_resources(self):
        return self.api_resources


class EntropyBlueprint(Blueprint):
    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 subdomain=None, url_defaults=None,
                 root_path=None):
        if '/' in name:
            raise Exception("Module name can't contain '/'")
        self.name = name
        self.quoted_name = quote(name)
        Blueprint.__init__(self, name, import_name, static_folder,
                           static_url_path, template_folder,
                           url_prefix='/{0}'.format(self.quoted_name),
                           subdomain=subdomain, url_defaults=url_defaults,
                           root_path=root_path)
        self.sys_info = None
        self.mod_parent = None
        self.register_routes()

    def register_routes(self):
        pass

    def set_mod_parent(self, mod_parent):
        """A way to set a link to the module the blueprint represents"""
        self.mod_parent = mod_parent

    def set_sys_info(self, sys_info):
        self.sys_info = sys_info

    def _get_global_data(self):
        """Global data to be available to all pages"""
        return self.sys_info
    global_data = property(_get_global_data)

    def render_template(self, template, **context):

        return render_template(template, module=self.mod_parent, globals=self.global_data, **context)




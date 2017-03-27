#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint

"""
blueprints
Created by otger on 27/03/17.
All rights reserved.
"""


class ModBlueprints(object):
    def __init__(self, parent):
        self.sys_info = None
        self.parent = parent
        self.blueprints = []

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


class EntropyBlueprint(Blueprint):
    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None,
                 root_path=None):
        Blueprint.__init__(self, name, import_name, static_folder,
                           static_url_path, template_folder,
                           url_prefix, subdomain, url_defaults,
                           root_path)

        self.sys_info = None
        self.mod_parent = None

    def set_mod_parent(self, mod_parent):
        """A way to set a link to the module the blueprint represents"""
        self.mod_parent = mod_parent

    def set_sys_info(self, sys_info):
        self.sys_info = sys_info

    def _get_global_data(self):
        """Global data to be available to all pages"""
        return {'mod_names': self.sys_info.mod_names}
    global_data=property(_get_global_data)


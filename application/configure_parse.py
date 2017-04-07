#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser


class ConfigBase(object):
    def __init__(self, filepath=None, section=None):
        self.section = section
        self.filepath = filepath
        self.cp = self.read_config(filepath)
        utils.ensure_dir(self.filepath)

    def read_config(self, filepath):
        cp = ConfigParser.ConfigParser()
        cp.read(filepath)
        return cp

    def get(self, option='', _default=None):
        try:
            res = self.cp.get(self.section, option)
        except Exception, e:
            res = _default
        return res

    def cp_set(self, option, value):
        if not self.cp.has_section(self.section):
            self.cp.add_section(self.section)

        self.cp.set(self.section, option, value)
        return self.cp

    def write_config(self):
        with open(self.filepath, 'w') as configfile:
            self.cp.write(configfile)


class ConfigManager(ConfigBase):
    def __init__(self, config_file):
        super(ConfigManager, self).__init__(config_file)

    def set_option(self, section, **kw):
        self.section = section
        for k, v in kw.iteritems():
            self.cp_set(k, v)
        self.write_config()

    def remove_section(self, section):
        self.cp.remove_section(section)
        self.write_config()

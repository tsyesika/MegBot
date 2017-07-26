##
# This is NOT the config, to get to that please look in config.py.example
##

##
#   This file is part of MegBot.
#
#   MegBot is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   MegBot is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with MegBot.  If not, see <http://www.gnu.org/licenses/>.
##

from types import *
import json
import os
import sys

from megbot.libraries.store import Store

CONFIG_FILE = "config.json"

class Configuration(Store):

    def __init__(self):
        self.fpath = os.path.join(os.getcwd(), CONFIG_FILE)
        self.mockConfigItem = ConfigItem(self, {})
        self._type = DictType

        if not os.path.isfile(self.fpath):
            print "[ErrorLine] You need to move config.json.example to %s" % self.fpath
            sys.exit()

        self._sfile = open(self.fpath)
        data = self._sfile.read()
        data = json.loads(data)
        self._sfile.close()

        self.data = data
        for item in self.data:
            if type(item) in [DictType, ListType]:
                # make it a ConfigItem
                self.data[item] = ConfigItem(self, self.data[item])

        self._sfile = None #holder

    def __setitem__(self, key, value):
        if type(value) != type(self.mockConfigItem):
            value = ConfigItem(self, value)

        super(Configuration, self).__setitem__(key, value)

        # because we're not setting much we really should be
        # saving it back to the config.
        self.save(True)

    def save(self, pretty=False):
        
        saveable = {}
        for item in self.data.keys():
            if type(self.data[item]) == type(self.mockConfigItem):
                saveable[item] = self.data[item].raw()
            else:
                saveable[item] = self.data[item]

        super(Configuration, self).save(pretty, data=saveable)

class ConfigItem(Store):
    def __init__(self, parent, item):
        self.data = item
        self.parent = parent
        for item in self.data:
            if type(item) in [ListType, DictType]:
                # make it a ConfigItem
                self.data[item] = ConfigItem(self, self.data[item])

    def __setitem__(self, key, value):
        self.data[key] = value
        self.parent.save(True)

    def raw(self):
        if type(self.data) == ListType:
            saveable = []
            for key in self.data:
                if type(key) == type(self.parent.mockConfigItem):
                    saveable.append(key.__dict__)
                else:
                    saveable.append(key)
        else:
            saveable = {}
            for key in self.data.keys():
                if type(self.data[key]) == type(self.parent.mockConfigItem):
                    saveable[key] = self.data[key].raw()
                else:
                    saveable[key] = self.data[key]
        return saveable

configuration = Configuration()

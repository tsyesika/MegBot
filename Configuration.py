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

import sys
import os
import json
from Libraries.store import Store
from types import *

class Configuration(Store):
    FILE = "config.json"

    def __init__(self):
        self.fpath = self.FILE
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
            item_type = type(item)
            if item_type == DictType or item_type == ListType:
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

class ConfigItem(Store):
    def __init__(self, parent, item):
        self.data = item
        for item in self.data:
            item_type = type(item)
            if item_type == DictType or item_type == ListType:
                # make it a ConfigItem
                self.data[item] = ConfigItem(self, self.data[item])

    def __setitem__(self, key, value):
        self.data[key] = value
        self.parent.save(True)

configuration = Configuration()

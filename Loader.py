#!/usr/bin/env python
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

from imp import load_source
import glob
import os

class LoaderError(Exception):
    pass # place holder

class Loader(object):
    _plugins = {}
    _path = ""

    def __init__(self):
        """ Initialises the Loader """
        pass            

    def load_plugin(self, name, plugin):
        """ Loads a specific plugin from a path """
        if not self._path:
            raise LoaderError("Path not defined")
        return load_source(name, plugin)

    def load_plugins(self):
        """ Will load ALL the plugins in the path """
        plugins = self.get_plugins()
        for plugin in plugins:
            name = self.get_name(plugin)
            self._plugins[name] = self.load_plugin(name, plugin)
        
        return self._plugins
    
    def get_plugins(self):
        """ Gets all the plugins in the path """
        return glob.glob("%s/*.py" % self._path)
    
    def get_name(self, plugin):
        """ Gets a name from a file name """
        return plugin.replace(".py", "")

    def set_path(self, plugin):
        """ Sets the path """
        path = os.path.splitext(
            os.path.basename(plugin)
        )[0]

        if "/" == path[-1]:
            # ends in / lets remove it.
            path = path[:-1]

        self._path = path
        return self._path

class CoreLoader(Loader):
    
    def set_path(self, plugin):
        """ Sets the path (including 'Core') """
        path = super(CoreLoader, self).set_path(plugin)
        print(path)
        self._path = "Core%s" % path
        return self._path

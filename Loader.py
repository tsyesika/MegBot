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

import glob
import os
import types
import os
import sys

from imp import load_source

class LoaderError(Exception):
    pass # place holder

class Loader(object):
    _plugins = {}
    _path = ""
    _prefix = "" # prepened to the plugin name
    _suffix = "" # appended to the plugin name

    def __init__(self, connection):
        """ Initialises the Loader """
        self.connection = connection

    def plugin_version(self, path):
        """ This will take a path and find a version identifier """
        # We'll use the modifier time on the file
        
        mtime = os.stat(path).st_mtime
        return mtime

    def is_new(self, name, path):
        """ This checks if a plugin has new things 
            (i.e. is it different from when we loaded it)
        """
        if name not in self._plugins:
            return True
    
        current_version = self.plugin_version(path)
        if self._plugins[name]["version"] == current_version:
            return False

        return True

    def get_path(self, name):
        """ Gets a plugin from it's name """
        if not self._path:
            raise LoaderError("Path must be set to deduce it from a name")
        
        return "%s%s" % (self._path, name)

    def load_plugin(self, name, plugin="", force=False):
        """ Loads a specific plugin from a path """
        if not self._path:
            raise LoaderError("Path not defined")
        
        if not plugin:
            plugin = self.get_path(name)

        # We don't want to reload if we don't need to
        if not (force or self.is_new(name, plugin)):
            return self._plugins[name]

        self.deconstruct_plugin(name)
        plugin = load_source(name, plugin)
        self.construct_plugin(plugin)

        return plugin

    def construct_plugin(self, plugin):
        """ This will construct a plugin if needed
        returns False if no constructor was called
        returns True if a constructor was called successfully
        """
        if not "init" in dir(plugin):
            # no constructor exists
            return False

        if not type(plugin.init)in [types.FunctionType, types.MethodType]:
            return False

        # we have a constructor of the right type
        plugin.init(self.connection)
        return True

    def deconstruct_plugin(self, name):
        """ Calls deconstructor if needed
        returns False if no deconstructor was called
        returns True if a deconstructor was called successfully
        """
        if not name in self._plugins:
            # didn't exist before
            return False

        if not "del" in dir(self._plugins[name]):
            # doesn't have desconstructor
            return False

        if not type(self._plugins[name].delete) in [types.FunctionType, 
                                                    types.MethodType]:
            # isn't a function.
            return False

        # okay we got a function that's our deconstructor
        self._plugins[name].delete(self.connection)
        return True

    def load_plugins(self, force=False):
        """ Will load ALL the plugins in the path """
        plugins = self.get_plugins()
        for plugin in plugins:
            name = self.get_name(plugin)
            self._plugins[name] = {
                "plugin":self.load_plugin(name, plugin=plugin, force=force),
                "version":self.plugin_version(plugin),
            }
        
        return self._plugins

    def get_plugins(self):
        """ Gets all the plugins in the path """
        return glob.glob("%s/*.py" % self._path)
    
    def get_name(self, plugin):
        """ Gets a name from a file name """
        plugin = plugin.replace(".py", "").split("/")[-1]
        plugin = self._prefix + plugin + self._suffix
        return plugin

    def normalize_path(self, plugin):
        """ Sets the path """
        path = os.path.splitext(
            os.path.basename(plugin)
        )[0]

        if "/" == path[-1]:
            # ends in / lets remove it.
            path = path[:-1]

        self._path = path
        return self._path
    
    def set_path(self, path):
        """ Sets the path of the loader 
        returns True if it succeeds
        returns False if it fails
        """
        
        self._path = path

        if not os.path.isdir(self._path):
            try:
                os.mkdir(self._path, 0775)
            except Exception:
                return False
        
        return True

    def __getitem__(self, key):
        """ Gets an plugin if it exists """
        return self._plugins[key]["plugin"]

    def __contains__(self, key):
        """ for when you do if blah in this """
        try:
            self._plugins[key]
            return True
        except KeyError:
            return False

class CoreLoader(Loader):
    _prefix = "Core"

    def load_plugin(self, name, plugin, force=False):
        """ Handles legacy - should be removed at some point """
        plugin = super(CoreLoader, self).load_plugin(name, plugin, force=force)

        # remove the Core prefix
        fmtname = name[4:]

        if "handler" == fmtname: 
            # new hook system
            setattr(self.connection, fmtname, plugin.Handler(self.connection))
        elif "hooker" == fmtname:
            # old hook system
            setattr(self.connection, fmtname, plugin.Hooker())
        return plugin

class PluginsLoader(Loader):
    
    def load_plugin(self, name, plugin, force=False):
        plugin = super(PluginsLoader, self).load_plugin(name, plugin, force=force)

        plugin.Web = self.connection.libraries["IRCObjects"].L_Web(self.connection)
        plugin.Helper = self.connection.libraries["IRCObjects"].L_Helper()
        plugin.Format = self.connection.libraries["IRCObjects"].L_Format()
        plugin.String = self.connection.libraries["String"].String 

        return plugin

class LibraryLoader(Loader):

    def set_path(self, path):
        """ 
        Sets the path as normal and then appends it to sys.paths
        So that you can import any of the libraries in the plugins
        """
        super(LibraryLoader, self).set_path(path)
        sys.path.append(path)


class Master_Loader(object):
    def __init__(self, connection, paths):
        """ This will make loaders on connection for paths """
        ## look for a way around this
        # this is to retain order so library is forced first.
        path_itr = paths.keys()
        path_itr.remove("libraries")
        path_itr.insert(0, "libraries")

        for path in path_itr:
            # is there a specialised loader.
            name = "%s%sLoader" % (path[0].upper(), path[1:])
            
            try:
                _tmp_loader = eval(name)
            except Exception:
                _tmp_loader = Loader
            finally:
                loader = _tmp_loader(connection)

            loader.set_path(paths[path])
            loader.load_plugins()
            setattr(connection, path.lower(), loader)

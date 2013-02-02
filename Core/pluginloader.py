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

"""This is to load plugins, if you leave plugin as the default (None)
it will go out and try and load them all. It doesn't return anything.
Instead of returning anything it adds the plugins directly onto the
connection by access through the connection parameter passed to main.
"""

import glob
import imp
import os

def main(connection, plugin=None):
    """
    This will load plugins, if plugin is left as the default (None) then
    it will look in Plugins/ (or what's specified in the config under
    the dict path). if it's specified it will only load that specific plugin.
    This will also add the Server, Helper and Web instances to the bots
    """
    if plugin:
        if "unload" in dir(connection.plugins[plugin]):
            connection.plugins[plugin].unload(connection)
        plugin_path = connection.config.paths["plugin"] + plugin + ".py"
        loaded_plugin = imp.load_source(plugin, plugin_path)
        connection.plugins[plugin] = loaded_plugin
        connection.Server = connection.server
        if "init" in dir(connection.plugins[plugin]):
            connection.plugins[plugin].init(connection)

    else:
        for plugfi in glob.glob(connection.config.paths["plugin"] + "*.py"):
            name = os.path.splitext(os.path.basename(plugfi))[0]
            connection.plugins[name] = imp.load_source(name, plugfi)

            plugin = connection.plugins[name]

            plugin.Server = connection.server
            plugin.Helper = connection.libraries["IRCObjects"].L_Helper()
            plugin.Web = connection.libraries["IRCObjects"].L_Web(connection)
            plugin.Format = connection.libraries["IRCObjects"].L_Format
            if "init" in dir(connection.plugins[name]):
                connection.plugins[name].init(connection)

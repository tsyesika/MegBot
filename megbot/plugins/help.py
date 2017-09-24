##
#This file is part of MegBot.
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

""" Displays a help message or a list of available commands """

def main(connection, info):
    # Older versions of megbot had an easy to use list of plugins. Recreate it here
    plugins = {}
    for plgn in connection.plugin.get_plugins():
        name = connection.plugin.get_name(plgn)
        if name in connection.plugin._plugins:
            plugins[name] = connection.plugin._plugins[name]["plugin"]

    if not info.args:
        # Generic list of plugins.
        if plugins:
            info.channel.send(u"%s: %s", info.nick, ", ".join(plugins.keys()))
        else:
            info.channel.send(u"%s: It seems no plugins are loaded, please speak to the bot admin.", info.nick)
    else:
        plugin = info.args[0]
        if plugin in plugins.keys():
            if "help" in dir(plugins[plugin]):
                if type(plugins[plugin].help) in [FunctionType, MethodType, UnboundMethodType]:
                    # It's a function
                    plugins[plugin].help(connection, info)
                elif type(plugins[plugin].help) in StringTypes:
                    # It's a string
                    info.channel.send(u"%s: %s", info.nick, plugins[plugin].help)
            else:
                info.channel.send(u"%s: Can't find any help for %s.", info.nick, plugin)
        else:
            info.channel.send(u"%s: Can't find plugin %s.", info.nick, plugin)

help = u"Displays a list of plugins or if a plugin is specified tries to get the help for that plugin"

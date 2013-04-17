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

def main(connection):
    if not Info.args:
        # Generic list of plugins.
        cout = ""
        amount = len(connection.plugins.keys())-1
        done = False
        for i, plugin_name in enumerate(connection.plugins.keys()):
            done = True
            if i == amount:
                cout += " & " + plugin_name
            else:
                cout += ", " + plugin_name
        if done:
            Channel.send(u"%s: %s", Info.nick, cout[2:])
        else:
            Channel.send(u"%s: It seems no plugins are loaded, please speak to the bot admin.", Info.nick)
    else:
        plugin = Info.args[0]
        if plugin in connection.plugins.keys():
            if "help" in dir(connection.plugins[plugin]):
                if type(connection.plugins[plugin].help) in [FunctionType, MethodType, UnboundMethodType]:
                    # It's a function
                    connection.plugins[plugin].help(connection, Info)
                elif type(connection.plugins[plugin].help) in StringTypes:
                    # It's a string
                    Channel.send(u"%s: %s", Info.nick, connection.plugins[plugin].help)
            else:
                Channel.send(u"%s: Can't find any help for %s.", Info.nick, plugin)
        else:
            Channel.send(u"%s: Can't find plugin %s.", Info.nick, plugin)

help = u"Displays a list of plugins or if a plugin is specified tries to get the help for that plugin"

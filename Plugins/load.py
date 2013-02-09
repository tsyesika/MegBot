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

import imp, os

def find_name(args):
    """
    Returns first argument in args which doesn't start with -
    """
    if not args:
        return
    if args[0][0] != "-":
        return args[0]
    return find_name(args[1:])

def main(connection, line):
    """
    Handles plugin reloading for Core, Libraries, Config and normal user plugins.
    This will handle flags within the IRC. If also the libraries are being reloaded the
    special case of Helper, Web and Server are re-seeded in all the plugins the bot has.

    Once an auth system is inplace the http:// loading needs adding & pastebin loading.
    """
    if not Info.args:
        Channel.send("You must give a plugin name")
        return
    
    # Lets look for flags
    # -c = core
    # -l = library
    # -C = config
    name = find_name(Info.args)
    
    if "-c" in Info.args:
        # Okay - core plugins because this is tied closely into
        # MegBot we will struggle not having two copies of this code
        # there for it is going to live here and in MegBot.
        # please update both places if you change it.
        fname = "Core%s" % name
        if "coreplugins" in connection.config.paths:
            cpath = connection.config.paths["coreplugins"]
        else:
            cpath = "Core/"
        cpath = "%s%s.py" % (cpath, name)
        if os.path.isfile(cpath):
            plugin = imp.load_source(
                            "Core%s" % fname,
                            cpath
                            )
            connection.core[fname] = plugin
        else:
            Channel.send("Can't find core plugin %s." % name)
            return

    elif "-l" in Info.args:
        # okay - libraries
        plugin = connection.core["Corelloader"].main(
                                                connection,
                                                name
                                                )
        if plugin:
            Channel.send("Oh no, something went wrong!")
            return
        connection.libraries[name] = plugin

    elif "-C" in Info.args:
        # okay - config
        if os.path.isfile('config.py'):
            try:
                plugin = imp.load_source('config', 'config.py')
            except:
                Channel.send("Oh no, something went wrong!")
        else:
            Channel.send("Oh no, I can't seem to find your config?")
            return
        connection.config = plugin
        connection.settings = plugin.networks[connection.name]

    elif name:
        plugin = connection.core["Corepluginloader"].main(
                                                        connection,
                                                        name
                                                       )
        if not plugin[0]:
            Channel.send(plugin[1])
        else:
            Channel.send("Plugin %s has been reloaded" % name)
    else:
        # this is probably where complete reloading should be.
        Channel.send("You need to enter a plugin to reload/load")
        return

    # Helper, Web & Server needs setting to all plugins. (Channel is set per call).
    if "-l" in Info.args:
        # Libraries.
        if name == "IRCObjects":
            connection.server = plugin.L_Server(connection)
            for p in connection.plugins.keys():
                p = connection.plugins[p]
                p.Web = plugin.L_Web(connection)
                p.Server = connection.server
                p.Helper = plugin.L_Helper()
                p.Format = plugin.L_Format
            # Okay all done.
        # Lets set the library in the bot
        connection.libraries[name] = plugin
        Channel.send("Library %s has been reloaded." % (name))
    elif "-C" in Info.args:
        # config.
        # Has the nick changed?
        Server.raw("NICK %s" % connection.settings["nick"])
        Channel.send("Config has been reloaded.")
    elif "-c" in Info.args:
        # core
        connection.core[name] = plugin
        Channel.send("Core plugin %s has been reloaded" % name[4:])

help = "Loads or reloads a plugin"

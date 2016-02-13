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

""" Loads a plugin, config, core plugin or library """

import json
import os

def find_name(args):
    """
    Returns first argument in args which doesn't start with -
    """
    if not args:
        return
    if args[0][0] != "-":
        return args[0]
    return find_name(args[1:])

def main(connection, info):
    """
    Handles plugin reloading for Core, Libraries, Config and normal user plugins.
    This will handle flags within the IRC. If also the libraries are being reloaded the
    special case of Helper, Web and Server are re-seeded in all the plugins the bot has.

    Once an auth system is inplace the http:// loading needs adding & pastebin loading.
    """
    if not info.args:
        Channel.send("You must give a plugin name")
        return
    
    # Lets look for flags
    # -c = core
    # -l = library
    # -C = config

    name = find_name(info.args)
    
    if "-a" in info.args and "-f" in info.args:
        connection.libraries.load_plugins(force=True) 
        connection.core.load_plugins(force=True)
        connection.plugins.load_plugins(force=True)
        Channel.send("Okay, everything should have re-loaded. Please check the term for errors")

    elif "-a" in info.args:
        connection.core.load_plugins(force=True)
        connection.libraries.load_plugins(force=True)
        connection.plugins.load_plugins(force=True)
        Channel.send("Okay, everything that needed to be re-loaded should have been. Please check the term for errors")

    elif "-b" in info.args and "-n" in info.args:
        # blacklist plugin for a specific network
        if "blacklist" in connection.settings:
            connection.settings["blacklist"].append(name)
        else:
            connection.settings["blacklist"] = [name]
        
        Channel.send(String("%s been added to the blacklist for %s network", name, connection.name))

    elif "-b" in info.args:
        # blacklist for all networks
        if "blacklist" in connection.config:
            connection.config["blacklist"].append(name)
        else:
            connection.config["blacklist"] = [name]
    
        Channel.send(String("%s has been added to the global blacklist", name))

    elif "-w" in info.args and "-n" in info.args:
        # adds to network specific whitelist
        if "whitelist" in connection.settings:
            connection.settings["whitelist"].append(name)
        else:
            connection.settings["whitelist"] = [name]

        Channel.send(String("%s has been added to the whitelist for %s network", name, connection.name))

    elif "-w" in info.args:
        # adds to whitelist for all networks
        if "whitelist" in connection.config:
            connection.config["whitelist"].append(name)
        else:
            connection.config["whitelist"] = [name]

        Channel.send(String("%s has been added to the global whitelist", name, connection.name))

    elif "-c" in info.args:
        if "-f" in info.args:
            force = True
        else:
            force = False
        
        if name:
            connection.core.load_plugin(name=name, force=force)
            Channel.send("%s should have re-loaded now, please check the terminal for errors" % name)
        else:
            connection.core.load_plugins(force=force)
            Channel.send("The core plugins should have re-loaded now, please check the term for errors")

    elif "-l" in info.args:
        if "-f" in info.args:
            force = True
        else:
            force = False

        if name:
            connection.libraries.load_plugin(name=name, force=force)
            Channel.send("%s should have re-loaded now, please check the terminal for errors" % name)
        else:
            Channel.send("The libraries should have been re-loaded now, please check the term for errors")
            connection.libraries.load_plugins(force=force)

    elif "-C" in info.args:
        # okay - config
        if os.path.isfile('config.json'):
            try:
                f = open("config.json", "r")
                plugin = json.loads(f.read())
                f.close()
            except Exception:
                Channel.send("Oh no, something went wrong!")
        else:
            Channel.send("Oh no, I can't seem to find your config?")
            return
        connection.config = plugin
        connection.settings = plugin[u"networks"][connection.name]

help = "Loads or reloads a plugin"

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

""" This will take a valid plugin and the raw IRC line (which caused the
    call to the plugin and pull out the args. Once the arguments have been
    pulled out it'll make a valid call to the plugin (in a thread so not to
    lock up the bot on plugins which take a long time to execute). The bot
    will stop a plugin's execution if it takes too long.
"""

import time
import threading

class KillableThread(threading.Thread):
    def kill_meh(self):
        """Raises an (hopefully) uncatchable SystemExit exceptoin"""
        raise SystemExit

def main(connection, command, plugin):
    """ This executes and manages plugin calls.
    This will kill the plugins execution after
    <x> numver of seconds to prevent lockup due to
    plugins executing and excess RAM useage and CPU time.
    """

    if "times" not in dir(connection):
        connection.times = {}
    else:
        clear(connection)

    # I think this will stop repeat calls to the same plugin from the same user?
    # Maybe? M
    if not command.message in connection.times.keys():
        call(connection, command, plugin)

def call(connection, command, plugin_name):
    """ Makes a call to a plugin (if needed) """

    # This checks that megbot is actually in the channel first.
    # If it isn't we'll just return out.
    if not command.channel in connection.channels:
        return

    # Turn line back into a string so we have something hash
    # Lets get the plugin we're going to deal with.
    plugin = connection.plugins[plugin_name][0]


    # We need to add the Info and Channel libraries to the plugin.
    plugin.Info = command
    plugin.Channel = connection.channels[command.channel]
    if plugin_name in connection.config[u"plugin_options"]:
        plugin.Config = connection.config[u"plugin_options"][plugin_name]
    else:
        plugin.Config = {}

    # Now lets make a thread for the plugin to run in.
    thread = KillableThread(target=plugin.main,
                              args=(connection,)
                             )
    connection.times[command.message] = [thread, time.time(), plugin_name]

    # And finally, we need to start it.
    connection.times[command.message][0].start()

def clear(connection):
    """ Clears the plugins that have timed out or finished """
    purge = []

    if "timeout" in connection.config:
        try:
            timeout = int(connection.config["timeout"])
            connection.config["timeout"] = timeout
        except:
            timeout = 30 #default
    else:
        timeout = 30 # default

    for plugincall in connection.times:
        plugin_name = connection.times[plugincall][2]
        po = connection.config[u"plugin_options"]
        if plugin_name in po:
            if "timeout" in po[plugin_name]:
                try:
                    ptout = int(po[plugin_name]["timeout"])
                except:
                    ptout = timeout
            else:
                ptout = timeout
        else:
            ptout = timeout
        if not connection.times[plugincall][0].isAlive():
            purge.append(connection.times[plugincall])
        elif (connection.times[plugincall][1] - time.time()) > ptout:
            connection.times[plugincall][0].kill_meh()
    for process in purge:
        del connection.times[plugincall]

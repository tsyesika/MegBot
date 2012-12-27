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

def main(connection, line, plugin):
    """ This executes and manages plugin calls.
    This will kill the plugins execution after
    <x> numver of seconds to prevent lockup due to
    plugins executing and excess RAM useage and CPU time.
    """

    if "times" not in dir(connection):
        connection.times = {}
    else:
        clear(connection)
    
    if not line in connection.times.keys():
        call(connection, line, plugin)

def call(connection, line, plugin_name):
    """ Makes a call to a plugin (if needed) """
    
    # This checks that megbot is actually in the channel first.
    # If it isn't we'll just return out.
    if line.split()[2] not in connection.channels:
        return

    # Lets get the plugin we're going to deal with.
    plugin = connection.plugins[plugin_name]

    
    # We need to add the Info and Channel libraries to the plugin.
    plugin.Info = connection.libraries["IRCObjects"].Info(line)
    plugin.Channel = connection.channels[line.split()[2]]
    
    # Now lets make a thread for the plugin to run in.
    thread = threading.Thread(target=plugin.main,
                              args=(connection, line)
                             )
    connection.times[line] = [thread, time.time(), plugin_name]

    # And finally, we need to start it.
    connection.times[line][0].start()

def clear(connection):
    """ Clears the plugins that have timed out or finished """
    purge = []
    for plugincall in connection.times:
        if (connection.times[plugincall][1] - time.time()) > 5:
            pass
            #connection.times[plugincall] - destroy me
        elif not connection.times[plugincall][0].isAlive():
            purge.append(connection.times[plugincall])
    for process in purge:
        del connection.times[plugincall]

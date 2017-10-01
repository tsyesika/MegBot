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

from threading import Thread
import logging


class KillableThread(Thread):
    def kill_meh(self):
        """Raises an (hopefully) uncatchable SystemExit exceptoin"""
        if not self.is_alive():
            raise SystemExit

def main(connection, command, plugin):
    """ This executes and manages plugin calls.
    This will kill the plugins execution after
    <x> numver of seconds to prevent lockup due to
    plugins executing and excess RAM useage and CPU time.
    """
    if "running_plugins" not in dir(connection):
        connection.running_plugins = {}
    else:
        clear(connection)

    # I think this will stop repeat calls to the same plugin from the same user?
    # Maybe? M
    if not command.message in connection.running_plugins.keys():
        call(connection, command, plugin)

def call(connection, command, plugin_name):
    """ Makes a call to a plugin (if needed) """

    # This checks that megbot is actually in the channel first.
    # If it isn't we'll just return out.
    if not command.channel_name in connection.channels:
        return

    # Turn line back into a string so we have something hash
    # Lets get the plugin we're going to deal with.
    plugin = connection.plugin[plugin_name]

    if not hasattr(plugin, "main"):
        return

    config = {}
    config.update(connection.config[u"plugin_options"]["__DEFAULTS__"])
    config.update(connection.config[u"plugin_options"].get(plugin_name, {}))

    # Now lets make a thread for the plugin to run in.
    try:
        thread = KillableThread(target=plugin.main,
                                  args=(connection, command)
                                 )
    except Exception:
        logging.exception("Could not start pluging %r", plugin)
        return

    # Start the plugin
    thread.start()

    timer = connection.core["Corehandler"].TimedEvent(config["timeout"],
                                                        thread.kill_meh,
                                                        command.message)

    connection.handler.register_event(timer)
    connection.running_plugins[command.message] = thread 

def clear(connection):
    """ Clears the plugins that have timed out or finished """
    purge = []

    for command in connection.running_plugins:
        if not connection.running_plugins[command].is_alive():
            connection.handler.unregister_event(command)
            purge.append(command)

    for command in purge:
        del connection.running_plugins[command]

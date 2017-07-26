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

"""This will handle the server to bot pings (not CTCP pings).
This will be called when the bot recives a ping, it checks it's
valid (by checking the first element). The server ping will look
like:

    PING :server.address.of.node

a valid responce should be:

    PONG :server.address.of.node

The argument after PONG should always be what the server sent us.
"""

eventID = "PingEvent"

def main(connection, command):
    """Handles the PINGS"""
    # this is deprecated, should be removed.
    if not command.args:
        # huh, what? :S
        # we probably should be logging this.
        return
    connection.core["Coreraw"].main(connection, "PONG %s" % command.args[0])

def on_PING(connection, info):
    """ Responds to a ping """

    # stop the timer
    connection.handler.unregister_event(eventID)

    # respond to ping
    connection.core["Coreraw"].main(connection, "PONG %s" % info.args[0])

    # reset the timer
    timer = connection.core["Corehandler"].TimedEvent(600, connection_died, eventID, [connection])
    connection.handler.register_event(timer)

def init(connection):

    # currently this doesn't work due to handler not existing yet.
    return

    eventInfo = connection.libraries["IRCObjects"].Info()
    eventInfo.action = "PING"
    
    event = connection.handler.IRCEvent(eventInfo, on_PING, eventID)
    connectiion.handler.register_event(event)

    timer = connection.core["Corehandler"].TimedEvent(1200, connection_died, eventID, [connection])
    connection.handler.register_event(timer)


def connection_died(connection):
    connection.running = False
